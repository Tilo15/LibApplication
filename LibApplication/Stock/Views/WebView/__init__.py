from LibApplication.View.Window import View
from LibApplication.View.Binding import Binding
from LibApplication.View.ChildView import ChildView
from LibApplication.View.Event import Event
from LibApplication.Stock.Services.WebKit import WebKitService

from gi.repository import WebKit2, Soup
import rx

@View("WebView.glade", "root")
class WebView:
    __title = Binding("title", "text")
    __is_loading = Binding("spinner", "active")

    can_go_back = Binding("back", "sensitive")
    can_go_forward = Binding("forward", "sensitive")
    show_controls = Binding("controls", "reveal_child")
    
    custom_charset = Binding(lambda s: s.webkit, "custom_charset")
    zoom_level = Binding(lambda s: s.webkit, "zoom_level")

    __web_kit_service = WebKitService

    @Binding("url", "text")
    def url(self, url):
        if(url != self.webkit.get_uri()):
            self.webkit.load_uri(url)
    
        return url

    def __init__(self, url="about:blank", profile = None):
        # Get the webkit context
        context = self.__web_kit_service.get_context(profile)

        # Create the webkit object
        self.webkit = WebKit2.WebView.new_with_context(context)

        # Attach signals
        self.webkit.connect("load_changed", self.__load_changed)
        self.webkit.connect("notify::title", self.__title_changed)
        self.webkit.connect("notify::uri", self.__url_changed)


        # Add the widget to the view
        self._root.add(self.webkit)
        self._root.set_child_packing(self.webkit, True, True, 0, 0)
        self.webkit.show()

        # Navigate to the page
        self.webkit.load_uri(url)


    def __load_changed(self, sender, data):
        # Update loading state
        self.__is_loading = self.webkit.is_loading()

        # Update forward and back states
        self.can_go_back = self.webkit.can_go_back()
        self.can_go_forward = self.webkit.can_go_forward()

        # Send event
        self.loading()

    def __title_changed(self, sender, data):
        self.__title = self.webkit.get_title()
        self.title()

    def __url_changed(self, sender, data):
        self.navigate(self.webkit.get_uri())

    @Event
    def go_back(self):
        print("yeet")
        if(self.can_go_back):
            self.webkit.go_back()
        
    @Event
    def go_forward(self):
        if(self.can_go_forward):
            self.webkit.go_forward()

    @Event
    def navigate(self, url):
        self.url = url
        return url

    @Event
    def loading(self):
        return self.__is_loading

    @Event
    def title(self):
        return self.__title

    def source(self):
        def get(observer):
            resource = self.webkit.get_main_resource()
            
            def got(resource, result, data):
                observer.on_next(resource.get_data_finish(result))
                observer.on_completed()

            resource.get_data(None, got, None)

        return rx.Observable.create(get)