.. _service_wrapper::
  
Service Wrapper
===============

The Service Wrapper is a class designed to wrap various methods of a Connection object with pre, post, and exception handlers, adding extra functionality to existing Connection methods. It allows users to extend and customize the behavior of specific Connection methods without modifying the original implementation.

Here are some typical use cases of service wrappers:

    - tracking the sequence/occurance of CLI command calls throughout a script

    - debug-logging the input arguments to, and output values from particular
      services.

    - building a LRU cache based on script inputs and device states.

    - etc.


Usage
-----

To use the Service Wrapper, follow these steps:

1) Create a child class derived from the `pyats.connections.ServiceWrapper` class. This child class will serve as the Service Wrapper for the desired Connection methods.

2) Set the `conn_type` and `service_name` of the child class to the Connection type and service name that the Service Wrapper will be applied to. This will typically be `unicon.Connection` and the name of the service method, such as `execute` or `configure`. The `order` class variable can also be set to determine the order in which the Service Wrappers will be applied.

3) Define the conditions under which the Service Wrapper should be applied to the service using the `applicable` method.

4) (Optional) Implement the necessary methods in the child class to define pre, post, and exception handling behavior. These methods will be executed at different stages during the service call.

5) (Optional) Use Testcase `Steps` to provide more robust reporting and leverage the pyATS reporter functionality.

6) (Optional) Configure CLI parser arguments in the child class using the `configure_parser` method. This is used to enable easy integration with CLI interfaces.

.. note:: 

    error handlers can suppress an exception, and/or track/register it 
    internally. By default the built-in error handler will simply raise the
    current exception. Developer can modify that to suppress the current 
    exception being handled, and return a fixed/altered result.


Service Wrapper Class
---------------------

The Service Wrapper base class provides several methods that can be overwritten by the user to customize the behavior of the service call:

`call_service`
``````````````

This method is responsible for calling the wrapped service. By default, it calls the service and passes any arguments that were provided to it. It returns the output of the service call, which can be utilized in the `post_service` method. If an error occurs, it calls the `exception_service` method. This method can be completely overloaded to change the behavior of the service call.

.. code-block:: python

  def call_service(self, *args, **kwargs) -> Any:
    """Call the service three times"""
    ret_list = []
    for _ in range(3):
        try:
            ret_list.append(self.service(*args, **kwargs))
        except Exception as e:
            logger.exception(f"Exception occurred: {e}")
    return ret_list

`exception_service`
```````````````````

The `exception_service` method is called if an exception occurs during the service call inside the `call_service` method. It is an abstracted method that will only run if the child class implements it. It can return anything to be used in the `post_service` method.

.. code-block:: python

  def exception_service(self, e: Exception, *args, **kwargs) -> Any:
    logger.exception(f"Exception occurred: {e}")
    return f'Exception occurred: {e}'

`pre_service`
`````````````

The `pre_service` method is called before the `call_service` method is executed. It is an abstracted method that will only run if the child class implements it. This method allows performing any necessary actions or setup before the actual service call.

.. code-block:: python

  def pre_service(self, *args, **kwargs) -> None:
    logger.info(f"Running pre_service on {self.service_name}")
    logger.info(f"{self.service_name} args: {args} kwargs: {kwargs}")

`post_service`
``````````````

The `post_service` method is called after the `call_service` method is executed. It is an abstracted method that will only run if the child class implements it. This method is used to handle any post-processing actions after the service call. It receives the output of the `call_service` method as an argument.

.. code-block:: python

  def post_service(self, output: Any, *args, **kwargs) -> None:
    logger.info(f"Running post_service on {self.service_name}")
    logger.info(f"{self.service_name} output: {output}")

`configure_parser`
``````````````````

The `configure_parser` method is called when the Service Wrapper is loaded. It is used to configure CLI parser arguments, similar to an easypy plugin. This is a classmethod that requires definition from the implementor. It takes in a `parser` argument, which is an instance of the `argparse.ArgumentParser` class.

.. code-block:: python

  @classmethod
  def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '--service-wrapper-arg',
        dest='service_wrapper_arg',
        action='store_true',
        help='Service Wrapper argument',
    )

    return parser

`applicable`
````````````

The `applicable` class method is used to determine whether the Service Wrapper should be applied to the service. This is also a classmethod that requires definition from the implementor. It takes in a `connection` argument, which is an instance of the `pyats.connections.BaseConnection` class. It should return a boolean value: `True` if the Service Wrapper should be applied, and `False` otherwise. 

This is in addition to the default `conn_type` and `service_name` checks that are done. This allows for more fine-grained control over which services the Service Wrapper is applied to. For example, the Service Wrapper can be applied to a specific device type, or only when a certain argument is passed to the service.

.. code-block:: python

  # Override applicable to check if the device is an IOSXE device
  @classmethod
  def applicable(cls, connection: BaseConnection, *args, **kwargs) -> bool:
    """Ensure the device OS is iosxe and the service wrapper argument is passed"""
    return connection.device.os == 'iosxe'

Important Attributes
````````````````````

The Service Wrapper base class also provides several attributes that can be used in the Service Wrapper methods:

- `self.service`
    - The service method that the Service Wrapper is applied to
    - Note that this should be exclusively used to call the wrapper services. You **cannot** call `self.execute` for example as this does not exist.
- `self.connection`
    - The Connection object that the Service Wrapper is applied to
    - Note that caution should be taken when calling wrapped attributes on the connection object. It's possible to create an infinite loop if the wrapped attribute is also wrapped by the Service Wrapper.
- `self.device`
    - The device object that the Connection object is connected to
- `self.logger`
    - The logger object that can be used to log messages specific to the Service Wrapper
- `self.testcase`
    - The testcase object that can be used to access testcase data
    - This is the same testcase object that is passed to easypy plugins and has access to testcase data through `self.testcase.parameters`
- `self.args`
    - The arguments as defined in the `configure_parser` method

Class Variables
```````````````

In addition to the methods, the Service Wrapper base class also provides several class variables that must be set to define which service the Service Wrapper will be applied to:

- `conn_type`
    - The Connection type that the Service Wrapper will be applied to. Options include
    
    .. code-block:: python

      # This is a catch-all for all Connection types
      pyats.connections.BaseConnection

      # This is the standard unicon connection
      unicon.Connection

      # Used for rest connections
      rest.connector.Rest

      # Used for yang connections
      yang.connector.Gnmi
      yang.connector.Netconf

- `service_name`
    - The service the wrapper will be used on. This will be the name of the service method, such as `execute` or `configure`

- `order`
    - This is an optional variable. It's is used to determine the order in which the Service Wrappers will be applied. It is an integer value, with higher values being applied first. The default value is `0`.

Examples
--------

Execute Service Wrapper - IOSXE Device
``````````````````````````````````````

This is an example of a service wrapper for wrapping the execute service on an IOSXE device

.. note:: This example wrapper will run for ALL IOSXE devices when this wrapper script is installed. If this wrapper is installed in a shared environment, be aware that it affects all user jobs and any IOSXE devices in use.

.. code-block:: python

  import unicon
  from pyats.connections import ServiceWrapper

  class ExampleWrapper(ServiceWrapper):
      conn_type = unicon.Connection
      service_name = 'execute'

      @classmethod
      def configure_parser(cls, parser) -> None:
          parser.add_argument(
              '--service-wrapper-arg',
              dest='service_wrapper_arg',
              action='store_true',
              help='Service Wrapper argument',
          )

          return parser

      @classmethod
      def applicable(cls, connection, *args, **kwargs) -> bool:
          return connection.device.os == 'iosxe'

      def pre_service(self, *args, **kwargs) -> None:
          self.logger.info(f"Running command: {args[0]} on {self.device.name}")

      def post_service(self, output, *args, **kwargs) -> None:
          self.logger.info(f"Output: {output}")

      def call_service(self, *args, **kwargs) -> Any:
          try:
              self.logger.info(f"Calling service: {self.service_name}")
              return self.service(*args, **kwargs)
          except Exception as e:
              return self.exception_service(e, *args, **kwargs)

      def exception_service(self, e, *args, **kwargs):
          self.logger.exception(f"Exception occurred: {e}")
          return f'Exception occurred: {e}'

Steps
-----

Inside of each service wrapper method you are able to pass a `steps` argument that will automatically pick up the Testcase's current `steps` object, which allows for use of the context manager style of reporting, failing, and passing a test.

.. code-block:: python

  with steps.start() as step:
    step.passed('Passed')

This can be used in any of the four service wrapper methods.

.. code-block:: python

  from pyats.connections import ServiceWrapper

  class ExampleWrapper(ServiceWrapper):
    @classmethod
    def applicable(cls, connection, *args, **kwargs) -> bool:
        return True

    def pre_service(self, steps, *args, **kwargs) -> None:
        with steps.start('Pre Service Step') as step:
            step.passed('Sucessfully ran pre service step')

    def post_service(self, output, steps, *args, **kwargs) -> None:
        with steps.start('Post Service Step') as step:
            step.passed('Sucessfully ran post service step')

    def call_service(self, steps, *args, **kwargs) -> None:
        with steps.start('Call Service Step') as step:
            step.passed('Sucessfully ran call service step')

    def exception_service(self, e, steps, *args, **kwargs) -> None:
        with steps.start('Exception Service Step') as step:
            step.passed('Sucessfully ran exception service step')

.. note:: The `steps` argument is only filled when the service wrapper is run in the context of a Testcase. If no Testcase is found, the `steps` argument will be `None`. Keep this in mind if your service wrapper is used in a standalone context with no Testcase.

Execution
---------

Configuration Method
````````````````````

Once the service wrapper is created, you can utilize it by adding it to the
pyats configuration file. You can read up on how to configure that 
:ref:`here. <pyats_configuration>`

.. code-block:: ini

  [service_wrapper]
  example_wrapper = path.to.module:ExampleWrapper

Entrypoint Method
`````````````````

Additionally, you can utilize it by adding it as an entry 
point in your package's setup file through the `pyats.connections.wrapper` 
entry point descriptor. This enables the service wrapper to be called and 
employed within the context of your package, facilitating seamless integration 
and utilization of the wrapped functionalities.

.. code-block:: python

  setup(
    ...,

    # console entry point
    entry_points = {
        'pyats.connections.wrapper': [
            'example_wrapper = path.to.path:ExampleWrapper'
          ]
      }
  )