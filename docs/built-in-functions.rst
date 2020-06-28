.. index:: function, built-in;

.. _built_in_functions:

Built in Functions
******************

Vyper provides a collection of built in functions available in the global namespace of all
contracts.

.. _functions:

.. py:function:: floor(value: decimal) -> int128

    Rounds a decimal down to the nearest integer.

    * ``value``: Decimal value to round down

.. py:function:: ceil(value: decimal) -> int128

    Rounds a decimal up to the nearest integer.

    * ``value``: Decimal value to round up

.. py:function:: convert(value, type_) -> Any

    Converts a variable or literal from one type to another.

    * ``value``: Value to convert
    * ``type_``: The destination type to convert to (``bool``, ``decimal``, ``int128``, ``uint256`` or ``bytes32``)

    Returns a value of the type specified by ``type_``.

    For more details on available type conversions, see :ref:`type_conversions`.

.. py:function:: empty(typename) -> Any

    Returns a value which is the default (zeroed) value of its type.

    * ``typename``: Name of the type

    For instance, `xs: uint256[5] = empty(uint256[5])`

.. py:function:: as_wei_value(value: int, unit: str) -> uint256

    Takes an amount of ether currency specified by a number and a unit and returns the integer quantity of wei equivalent to that amount.

    * ``value``: Value for the ether unit
    * ``unit``: Ether unit name (e.g. ``"wei"``, ``"ether"``, ``"gwei"``, etc.) indicating the denomination of ``value``.

.. py:function:: slice(b: Union[bytes, bytes32, string], start: uint256, length: uint256) -> Union[bytes, string]

    Copy a list of bytes and return a specified slice.

    * ``b``: value being sliced
    * ``start``: start position of the slice
    * ``length``: length of the slice

    If the value being sliced is a ``bytes`` or ``bytes32``, the return type is ``bytes``.  If it is a ``string``, the return type is ``string``.

    .. code-block:: python

        @public
        @view
        def foo(s: string[32]) -> string[5]:
            return slice(s, 4, 5)

    .. code-block:: python

        >>> ExampleContract.foo("why hello! how are you?")
        "hello"

.. py:function:: len(b: Union[bytes, string]) -> uint256

    Return the length of a given ``bytes`` or ``string``.

    .. code-block:: python

        @public
        @view
        def foo(s: string[32]) -> uint256:
            return len(s)

    .. code-block:: python

        >>> ExampleContract.foo("hello")
        5

.. py:function:: concat(a, b, *args) -> bytes

    Takes 2 or more bytes arrays of type ``bytes32`` or ``bytes`` and combines them into a single ``bytes`` list.

.. py:function:: keccak256(value) -> bytes32

    Returns a ``keccak256`` hash of the given value.

    * ``value``: Value to hash. Can be ``str_literal``, ``bytes``, or ``bytes32``.

.. py:function:: sha256(value) -> bytes32

    Returns a ``sha256`` (SHA2 256bit output) hash of the given value.

    * ``value``: Value to hash. Can be ``str_literal``, ``bytes``, or ``bytes32``.

.. py:function:: uint256_addmod(a: uint256, b: uint256, c: uint256) -> uint256

    Returns the modulo of ``(a + b) % c``. Reverts if ``c == 0``.

.. py:function:: uint256_mulmod(a: uint256, b: uint256, c: uint256) -> uint256

    Returns the modulo from ``(a * b) % c``. Reverts if ``c == 0``.

.. py:function:: sqrt(d: decimal) -> decimal

    Returns the square root of the provided decimal number, using the Babylonian square root algorithm.

.. py:function:: method_id(method, output_type: type = bytes[4]) -> Union[bytes32, bytes[4]]

    Takes a function declaration and returns its method_id (used in data field to call it).

    * ``method``: Method declaration as given as a literal string
    * ``output_type``: The type of output (``bytes[4]`` or ``bytes32``). Defaults to ``bytes[4]``.

    Returns a value of the type specified by ``output_type``.

    .. code-block:: python

        @public
        @view
        def foo() -> bytes[4]:
            return method_id('transfer(address,uint256)', output_type=bytes[4])

    .. code-block:: python

        >>> ExampleContract.foo("hello")
        b"\xa9\x05\x9c\xbb"

.. py:function:: ecrecover(hash: bytes32, v: uint256, r: uint256, s: uint256) -> address

    Recovers the address associated with the public key from the given elliptic curve signature.

    * ``r``: first 32 bytes of signature
    * ``s``: second 32 bytes of signature
    * ``v``: final 1 byte of signature

    Returns the associated address, or ``0`` on error.

.. py:function:: ecadd(a: uint256[2], b: uint256[2]) -> uint256[2]

    Takes two points on the Alt-BN128 curve and adds them together.

.. py:function:: ecmul(point: uint256[2], scalar: uint256) -> uint256[2]

    Takes a point on the Alt-BN128 curve (``p``) and a scalar value (``s``), and returns the result of adding the point to itself ``s`` times, i.e. ``p * s``.

    * ``point``: Point to be multiplied
    * ``scalar``: Scalar value

.. py:function:: extract32(b: bytes, start: int128, output_type=bytes32) -> Union[bytes32, int128, address]

    Extract a value from a ``bytes`` list.

    * ``b``: ``bytes`` list to extract from
    * ``start``: Start point to extract from
    * ``output_type``: Type of output (``bytes32``, ``int128``, or ``address``). Defaults to ``bytes32``.

    Returns a value of the type specified by ``output_type``.

    .. code-block:: python

        @public
        @view
        def foo(bytes[32]) -> address:
            return extract32(b, 12, output_type=address)

    .. code-block:: python

        >>> ExampleContract.foo("0x0000000000000000000000009f8F72aA9304c8B593d555F12eF6589cC3A579A2")
        "0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2"


Low Level Built in Functions
****************************

Vyper contains a set of built in functions which execute opcodes such as ``SEND`` or ``SELFDESTRUCT``.

.. py:function:: send(to: address, value: uint256) -> None

    Sends ether from the contract to the specified Ethereum address.

    * ``to``: The destination address to send ether to
    * ``value``: The wei value to send to the address

    .. note::

        The amount to send is always specified in ``wei``.

.. py:function:: raw_call(to: address, data: bytes, max_outsize: int = 0, gas: uint256 = gasLeft, value: uint256 = 0, is_delegate_call: bool = False, is_static_call: bool = False) -> bytes[max_outsize]

    Calls to the specified Ethereum address.

    * ``to``: Destination address to call to
    * ``data``: Data to send to the destination address
    * ``max_outsize``: Maximum length of the bytes array returned from the call. If the returned call data exceeds this length, only this number of bytes is returned.
    * ``gas``: The amount of gas to attach to the call. If not set, all remainaing gas is forwarded.
    * ``value``: The wei value to send to the address (Optional, default ``0``)
    * ``is_delegate_call``: If ``True``, the call will be sent as ``DELEGATECALL`` (Optional, default ``False``)
    * ``is_static_call``: If ``True``, the call will be sent as ``STATICCALL`` (Optional, default ``False``)

    Returns the data returned by the call as a ``bytes`` list, with ``max_outsize`` as the max length.

    Returns ``None`` if ``max_outsize`` is omitted or set to ``0``.

    .. note::

        The actual size of the returned data may be less than ``max_outsize``. You can use ``len`` to obtain the actual size.

.. py:function:: selfdestruct(to: address) -> None

    Triggers the ``SELFDESTRUCT`` opcode (``0xFF``), causing the contract to be destroyed.

    * ``to``: Address to forward the contract's ether balance to

    .. warning::

        This method will delete the contract from the Ethereum blockchain. All non-ether assets associated with this contract will be "burned" and the contract will be inaccessible.

.. py:function:: raise(reason: str = None) -> None

    Raises an exception.

    * ``reason``: The exception reason

    This method triggers the ``REVERT`` opcode (``0xFD``) with the provided reason given as the error message. The code will stop operation, the contract's state will be reverted to the state before the transaction took place and the remaining gas will be returned to the transaction's sender.

    If the reason string is set to ``UNREACHABLE``, an ``INVALID`` opcode (``0xFE``) will be used instead of ``REVERT``. In this case, calls that revert will not receive a gas refund.

    .. note::

        To give it a more Python-like syntax, the raise function can be called without parenthesis, the syntax would be ``raise "An exception"``. Even though both options will compile, it's recommended to use the Pythonic version without parentheses.

.. py:function:: assert(cond: bool, reason: str = None) -> None

    Asserts the specified condition.

    * ``cond``: The boolean condition to assert
    * ``reason``: The exception reason

    This method's behavior is equivalent to:

    .. code-block:: python

        if not cond:
            raise "reason"

    The only difference in behavior is that ``assert`` can be called without a reason string, while ``raise`` requires one.

    If the reason string is set to ``UNREACHABLE``, an ``INVALID`` opcode (``0xFE``) will be used instead of ``REVERT``. In this case, calls that revert will not receive a gas refund.

    .. note::

        To give it a more Python-like syntax, the assert function can be called without parenthesis, the syntax would be ``assert your_bool_condition``. Even though both options will compile, it's recommended to use the Pythonic version without parenthesis.

.. py:function:: raw_log(topics: bytes32[4], data: bytes) -> None

    Provides low level access to the ``LOG`` opcodes, emitting a log without having to specify an ABI type.

    * ``topics``: List of ``bytes32`` log topics
    * ``data``: Unindexed event data to include in the log, bytes or bytes32

    This method provides low-level access to the ``LOG`` opcodes (``0xA0``..``0xA4``). The length of ``topics`` determines which opcode will be used. ``topics`` is a list of bytes32 topics that will be indexed. The remaining unindexed parameters can be placed in the ``data`` parameter.


.. py:function:: create_forwarder_to(target: address, value: uint256 = 0) -> address

    Duplicates a contract's code and deploys it as a new instance, by means of a ``DELEGATECALL``.

    * ``target``: Address of the contract to duplicate
    * ``value``: The wei value to send to the new contract address (Optional, default 0)

    Returns the address of the duplicated contract.

.. py:function:: blockhash(block_num: uint256) -> bytes32

    Returns the hash of the block at the specified height.

    .. note::

        The EVM only provides access to the most 256 blocks. This function will return 0 if the block number is greater than or equal to the current block number or more than 256 blocks behind the current block.
