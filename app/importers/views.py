from django.shortcuts import render
from django.contrib import messages

from .Importer import Importer
from .FileParser import FileParser
from .models import FileStorage


def file_upload(request):
    if request.method == "POST" and request.FILES["file"]:
        _file = request.FILES["file"]
        file_obj = FileStorage(file_name=_file.name, file_path=_file)
        file_obj.save()
        parser = FileParser(file=file_obj.file_path)
        parser.run()
        errors = parser.errors
        if len(errors) > 20:
            errors = errors[0:21]
        for err in errors:
            messages.warning(request, err)
        db_data = parser.get_parsed_data()
        if db_data:
            importer = Importer(data=db_data, file_id=file_obj.id)
            error = None
            try:
                importer.run()
            except Exception as exc:
                error = f"Error importing data to database, error message: {exc}"
            if error:
                messages.warning(request, error)
            else:
                messages.success(request, "File imported to database")
    return render(request, "importers/upload.html")

