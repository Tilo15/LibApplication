# LibApplication

LibApplication is a work in progress library to ease the development of GTK3 applications in Python. It's goal is to offer a reusable view system that was inspired by Angular2 components, as well as to be a general purpose framework for Linux desktop applications.

## Progress

At this stage, this list may change around a bit. These are the currently planned features

- [x] Views
  - [x] Property binding
  - [x] Formatted property binding
  - [x] Child view (Inserting one view into another)
  - [x] Child views (Inserting many views into another)
    - [ ] Better support for GTK Stack
    - [ ] Functionality for filtering items
  - [ ] Stock views
  - [ ] Event support
  - [ ] Special support for toplevels
- [ ] Services
  - [ ] Dependancy injection
  - [ ] Stock services
    - [ ] Http (python-requests)
    - [ ] User storage
    - [ ] DBus
  - [ ] Integration with libraries build with LibMedium
- [ ] App
  - [ ] Configuration
  - [ ] File open notifications
  - [ ] Launcher action notifications

## Notes

This is still very much in development and is not ready for producation. Code and APIs need to be tidied up and will change a lot before considered stable.