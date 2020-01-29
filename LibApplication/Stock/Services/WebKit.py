from LibApplication.Service import Service
from LibApplication.Loop.Queue import QueueLoop
from LibApplication.Loop.AsTask import AsTask
from LibApplication.Stock.Services.Application import ApplicationService

from gi.repository import WebKit2, Soup

import os

@Service
class WebKitService:

    application_service = ApplicationService

    def __init__(self):
        self.contexts = {}

        self.contexts[None] = self.get_context("default")

    def get_context(self, key):
        if(key in self.contexts):
            return self.contexts[key]

        context_data_path = os.path.join(self.application_service.data_path, "WebKit", key)

        data_manager = WebKit2.WebsiteDataManager(base_cache_directory = os.path.join(context_data_path, "cache"),
                                  base_data_directory = os.path.join(context_data_path, "data"),
                                  disk_cache_directory = os.path.join(context_data_path, "disk"),
                                  indexeddb_directory = os.path.join(context_data_path, "indexed_db"),
                                  local_storage_directory = os.path.join(context_data_path, "local_storage"),
                                  offline_application_cache_directory = os.path.join(context_data_path, "application_cache"),
                                  websql_directory = os.path.join(context_data_path, "websql"),
                                  is_ephemeral = False)

        context = WebKit2.WebContext.new_with_website_data_manager(data_manager)

        cookie_manager = context.get_cookie_manager()
        cookie_manager.set_accept_policy(WebKit2.CookieAcceptPolicy.ALWAYS)
        cookie_manager.set_persistent_storage(os.path.join(context_data_path, "cookies.db"), WebKit2.CookiePersistentStorage.SQLITE)
        
        self.contexts[key] = context

        return context
        