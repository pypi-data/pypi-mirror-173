import uuid
from copy import deepcopy
from typing import List, Union

from licenseware.constants.states import States
from licenseware.constants.uploader_types import (
    FileValidationResponse,
    ValidationResponse,
)
from licenseware.constants.web_response import WebResponse
from licenseware.uploader.validation_parameters import UploaderValidationParameters
from licenseware.utils.file_upload_handler import FileUploadHandler

from .helpers import get_error_message, get_failed_validations, get_filenames_response


def default_filecontents_validation_handler(
    files: Union[List[bytes], List[str]],
    validation_parameters: UploaderValidationParameters,
) -> WebResponse:

    if not isinstance(
        validation_parameters, UploaderValidationParameters
    ):  # pragma no cover
        validation_parameters = UploaderValidationParameters(**validation_parameters)

    filename_validation_response = get_filenames_response(
        deepcopy(files), validation_parameters
    )
    if filename_validation_response is not None:
        return filename_validation_response  # pragma: no cover

    validation_response = []
    for file in files:

        f = FileUploadHandler(file)

        if validation_parameters.ignore_filenames is not None:
            if f.filename in validation_parameters.ignore_filenames:  # pragma: no cover
                continue

        failed_validations = get_failed_validations(f, validation_parameters)

        if not failed_validations:
            validation_response.append(
                ValidationResponse(
                    status=States.SUCCESS,
                    filename=f.filename,
                    message=validation_parameters.filename_valid_message,
                )
            )
        else:
            validation_response.append(  # pragma: no cover
                ValidationResponse(
                    status=States.FAILED,
                    filename=f.filename,
                    message=get_error_message(failed_validations),
                )
            )

    file_response = FileValidationResponse(
        event_id=str(uuid.uuid4()),
        status=States.SUCCESS,
        message="File names and contents were analysed",
        validation=tuple(validation_response),
    )

    return WebResponse(content=file_response, status_code=200)
