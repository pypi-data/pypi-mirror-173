Modules gating
==============

Every successfully built module is moved to the ``done`` state. Modules in this state cannot
be used as a build dependency for other modules. They need to be moved to the ``ready`` state.

By default, MBS moves the module from the ``done`` state to the ``ready`` state automatically.
The Koji resolver, if used, will handle gating naturally.
