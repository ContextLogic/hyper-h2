# -*- coding: utf-8 -*-
"""
h2/exceptions
~~~~~~~~~~~~~

Exceptions for the HTTP/2 module.
"""
import h2.errors


class H2Error(Exception):
    """
    The base class for all exceptions for the HTTP/2 module.
    """


class ProtocolError(H2Error):
    """
    An action was attempted in violation of the HTTP/2 protocol.
    """
    #: The error code corresponds to this kind of Protocol Error.
    error_code = h2.errors.PROTOCOL_ERROR


class FrameTooLargeError(ProtocolError):
    """
    The frame that we tried to send or that we received was too large.
    """
    #: This error code that corresponds to this kind of Protocol Error.
    error_code = h2.errors.FRAME_SIZE_ERROR


class FrameDataMissingError(ProtocolError):
    """
    The frame that we received is missing some data.

    .. versionadded:: 2.0.0
    """
    #: The error code that corresponds to this kind of Protocol Error
    error_code = h2.errors.FRAME_SIZE_ERROR


class TooManyStreamsError(ProtocolError):
    """
    An attempt was made to open a stream that would lead to too many concurrent
    streams.
    """
    pass


class FlowControlError(ProtocolError):
    """
    An attempted action violates flow control constraints.
    """
    #: The error code that corresponds to this kind of
    #: :class:`ProtocolError <h2.exceptions.ProtocolError>`
    error_code = h2.errors.FLOW_CONTROL_ERROR


class StreamIDTooLowError(ProtocolError):
    """
    An attempt was made to open a stream that had an ID that is lower than the
    highest ID we have seen on this connection.

    For backwards-compatibility reasons, this is also a subclass of
    ``ValueError``.
    """
    # TODO: Remove inheritance from ValueError.
    def __init__(self, stream_id, max_stream_id):
        #: The ID of the stream that we attempted to open.
        self.stream_id = stream_id

        #: The current highest-seen stream ID.
        self.max_stream_id = max_stream_id

    def __str__(self):
        return "StreamIDTooLowError: %d is lower than %d" % (
            self.stream_id, self.max_stream_id
        )


class NoAvailableStreamIDError(ProtocolError):
    """
    There are no available stream IDs left to the connection. All stream IDs
    have been exhausted.

    .. versionadded:: 2.0.0
    """
    pass


class NoSuchStreamError(ProtocolError):
    """
    A stream-specific action referenced a stream that does not exist.

    .. versionchanged:: 2.0.0
       Became a subclass of :class:`ProtocolError
       <h2.exceptions.ProtocolError>`
    """
    def __init__(self, stream_id):
        #: The stream ID that corresponds to the non-existent stream.
        self.stream_id = stream_id


class StreamClosedError(NoSuchStreamError):
    """
    A more specific form of
    :class:`NoSuchStreamError <h2.exceptions.NoSuchStreamError>`. Indicates
    that the stream has since been closed, and that all state relating to that
    stream has been removed.
    """
    def __init__(self, stream_id):
        #: The stream ID that corresponds to the nonexistent stream.
        self.stream_id = stream_id

        #: The relevant HTTP/2 error code.
        self.error_code = h2.errors.STREAM_CLOSED

        # Any events that internal code may need to fire. Not relevant to
        # external users that may receive a StreamClosedError.
        self._events = []


class InvalidSettingsValueError(ProtocolError, ValueError):
    """
    An attempt was made to set an invalid Settings value.

    .. versionadded:: 2.0.0
    """
    def __init__(self, msg, error_code):
        super(InvalidSettingsValueError, self).__init__(msg)
        self.error_code = error_code


class InvalidBodyLengthError(ProtocolError):
    """
    The remote peer sent more or less data that the Content-Length header
    indicated.

    .. versionadded:: 2.0.0
    """
    def __init__(self, expected, actual):
        self.expected_length = expected
        self.actual_length = actual

    def __str__(self):
        return "InvalidBodyLengthError: Expected %d bytes, received %d" % (
            self.expected_length, self.actual_length
        )
