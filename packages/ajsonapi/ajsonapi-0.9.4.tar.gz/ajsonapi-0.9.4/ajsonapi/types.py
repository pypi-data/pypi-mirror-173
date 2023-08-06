# Copyright © 2018-2020 Roel van der Goot
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""Module types provided types that can be used in the Attribute constructor.
"""

from datetime import datetime
from json import dumps, loads
from urllib.parse import unquote

from ajsonapi.conversions import id_name_to_number

Now = 'CuRrEnT_TiMeStAmP'  # pylint:disable=invalid-name


class Type:
    """Abstract base class for supported database types."""

    @staticmethod
    def from_json(value):
        """Converts a JSON value to the corresponding Python value."""
        return value

    @staticmethod
    def to_json(value):
        """Converts a Python value to the corresponding JSON value."""
        return value

    @staticmethod
    def to_sql(value):
        """Converts a Python value to the corresponding SQL attribute value."""
        return value

    @staticmethod
    def from_sql(value):
        """Converts an SQL attribute value to the corresponding Python value."""
        return value

    @staticmethod
    def from_qp(value):
        """Converts a query parameter to the corresponding Python value."""
        return value

    @staticmethod
    def sql(value):
        """Converts value into sql value."""
        return value


class Bool(Type):
    """Type for booleans."""

    name = 'BOOLEAN'

    @staticmethod
    def from_qp(value):
        if value == 'true':
            return True
        if value == 'false':
            return False
        if value == 'NULL':
            return None
        raise AttributeError(f"'Bool' type has no value '{value}'")

    @staticmethod
    def sql(value):
        if value:
            return 'TRUE'
        if value is False:
            return 'FALSE'
        # Must be None
        return 'NULL'


# Deprecating
Boolean = Bool


class DateTime(Type):
    """Type for date times."""

    name = 'TIMESTAMP'

    @staticmethod
    def sql(value):
        if value == Now:
            return 'current_timestamp'
        return f"'{value.isoformat()}'"

    @staticmethod
    def from_json(value):
        return datetime.fromisoformat(value).replace(tzinfo=None)

    @staticmethod
    def to_json(value):
        return value.isoformat()

    @staticmethod
    def from_qp(value):
        return datetime.fromisoformat(value).replace(tzinfo=None)


class DateTimeTZ(Type):
    """Type for date times with time zone information."""

    name = 'TIMESTAMP WITH TIME ZONE'

    @staticmethod
    def sql(value):
        if value == Now:
            return 'current_timestamp'
        return f"'{value.isoformat()}'"

    @staticmethod
    def from_json(value):
        return datetime.fromisoformat(value)

    @staticmethod
    def to_json(value):
        return value.isoformat()

    @staticmethod
    def from_qp(value):
        return datetime.fromisoformat(value)


# Deprecating
DateTimeTimeZone = DateTimeTZ


class Float32(Type):
    """Type for 32 bit floating point numbers."""

    name = 'FLOAT'

    @staticmethod
    def from_qp(value):
        return float(value)

    @staticmethod
    def sql(value):
        return str(value)


class Float64(Type):
    """Type for 64 bit floating point numbers."""

    name = 'DOUBLE PRECISION'

    @staticmethod
    def from_qp(value):
        return float(value)

    @staticmethod
    def sql(value):
        return str(value)


class Int16(Type):
    """Type for 16 bit signed integers."""

    name = 'SMALLINT'

    @staticmethod
    def from_qp(value):
        return int(value)

    @staticmethod
    def sql(value):
        return str(value)


class Int32(Type):
    """Type for 32 bit signed integers."""

    name = 'INT'

    @staticmethod
    def from_qp(value):
        return int(value)

    @staticmethod
    def sql(value):
        return str(value)


class Int64(Type):
    """Type for 64 bit signed integers."""

    name = 'BIGINT'

    @staticmethod
    def from_qp(value):
        return int(value)

    @staticmethod
    def sql(value):
        return str(value)


class Json(Type):
    """Type for json data."""

    name = 'JSONB'

    @staticmethod
    def sql(value):
        return f"'{dumps(value)}'"

    @staticmethod
    def to_sql(value):
        return dumps(value)

    @staticmethod
    def from_sql(value):
        if value is None:
            return None
        return loads(value)

    @staticmethod
    def from_qp(value):
        return loads(value)


class Numeric(Type):
    """Type for arbitrary precision numbers."""

    name = 'NUMERIC'

    @staticmethod
    def With(*, precision, scale=None):  # pylint: disable=invalid-name
        """Factory for SQL NUMERIC(precision, scale) types."""

        class NumericWith(Type):
            """Type for SQL NUMERIC(precision, scale) types."""

            name = f'NUMERIC({precision}, {scale})' if scale is not None else \
                    f'NUMERIC({precision})'

        return NumericWith


class String(Type):
    """Type for strings."""

    name = 'TEXT'

    @staticmethod
    def sql(value):
        sql_value = value.replace("'", "''")
        return f"'{sql_value}'"

    @staticmethod
    def from_qp(value):
        return unquote(value)

    @staticmethod
    def With(*, max_length):  # pylint: disable=invalid-name
        """Factory for SQL VARCHAR(max_length) types."""

        class StringWith(Type):
            """Type for SQL VARCHAR(max_length) types."""

            name = f'VARCHAR({max_length})'

            @staticmethod
            def sql(value):
                sql_value = value.replace("'", "''")
                return f"'{sql_value}'"

            @staticmethod
            def from_qp(value):
                return unquote(value)

        return StringWith


class Uuid(Type):
    """Type for uuids."""

    name = 'UUID'

    @staticmethod
    def from_qp(value):
        return id_name_to_number(value)
