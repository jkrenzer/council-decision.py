from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

from typing import (
    Any,
    Callable,
)

from pydantic_core import core_schema
from typing_extensions import Annotated, cast

from pydantic import (
    BaseModel,
    GetJsonSchemaHandler,
    ValidationError,
)
from pydantic.json_schema import JsonSchemaValue

from council_decision.crypto.dump_password import DumpPassword


class _EllipticCurvePrivateKeyPydanticAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        """
        We return a pydantic_core.CoreSchema that behaves in the following ways:

        * ints will be parsed as `ThirdPartyType` instances with the int as the x attribute
        * `ThirdPartyType` instances will be parsed as `ThirdPartyType` instances without any changes
        * Nothing else will pass validation
        * Serialization will always return just an int
        """

        def validate_from_byte(value: bytes) -> ec.EllipticCurvePrivateKey:
            return cast(
                ec.EllipticCurvePrivateKey,
                serialization.load_pem_private_key(
                    value,
                    password=DumpPassword.get(),
                ),
            )

        from_byte_schema = core_schema.chain_schema(
            [
                core_schema.bytes_schema(),
                core_schema.no_info_plain_validator_function(validate_from_byte),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_byte_schema,
            python_schema=core_schema.union_schema(
                [
                    # check if it's an instance first before doing any further work
                    core_schema.is_instance_schema(ec.EllipticCurvePrivateKey),
                    from_byte_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.BestAvailableEncryption(
                        DumpPassword.get()
                    ),
                )
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        # Use the same schema that would be used for `int`
        return handler(core_schema.bytes_schema())


EllipticCurvePrivateKey = Annotated[
    ec.EllipticCurvePrivateKey, _EllipticCurvePrivateKeyPydanticAnnotation
]


class _EllipticCurvePublicKeyPydanticAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        """
        We return a pydantic_core.CoreSchema that behaves in the following ways:

        * ints will be parsed as `ThirdPartyType` instances with the int as the x attribute
        * `ThirdPartyType` instances will be parsed as `ThirdPartyType` instances without any changes
        * Nothing else will pass validation
        * Serialization will always return just an int
        """

        def validate_from_byte(value: bytes) -> ec.EllipticCurvePublicKey:
            return cast(
                ec.EllipticCurvePublicKey,
                serialization.load_pem_public_key(value),
            )

        from_byte_schema = core_schema.chain_schema(
            [
                core_schema.bytes_schema(),
                core_schema.no_info_plain_validator_function(validate_from_byte),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_byte_schema,
            python_schema=core_schema.union_schema(
                [
                    # check if it's an instance first before doing any further work
                    core_schema.is_instance_schema(ec.EllipticCurvePublicKey),
                    from_byte_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.PKCS1,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        # Use the same schema that would be used for `int`
        return handler(core_schema.bytes_schema())


EllipticCurvePublicKey = Annotated[
    ec.EllipticCurvePublicKey, _EllipticCurvePublicKeyPydanticAnnotation
]
