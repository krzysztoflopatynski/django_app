import json

from django.shortcuts import render

from importers.models import DumpFileData
from importers.models import FileStorage


def report_view(request):
    files = FileStorage.objects.all().order_by('-timestamp')
    context = {
        "data": [],
        "files": files
    }
    if request.method == "GET":
        return render(request, "reports/report.html", context)
    else:
        file_id = request.POST['file_selector']
        data = prepare_report_data(file_id)
        context["data"] = json.dumps(data)
        if not data:
            context["message"] = "Data for given file is not available"
        return render(request, "reports/report.html", context)


BENFORD_MAPPING = {
    1: 30.1,
    2: 17.6,
    3: 12.5,
    4: 9.7,
    5: 7.9,
    6: 6.7,
    7: 5.8,
    8: 5.1,
    9: 4.6,
}

TOOLTIP_CONTAINER = "<div style='padding:10px; white-space: nowrap;'>{content}</div>"

TOOLTIP_ACTUAL = "<b>number:</b> {number}<br><b>occurrences:</b> {occurrences}<br>" \
                 "<b>occurrences[%]:</b> {percentage:.2f}<br><b>margin[%]:</b> {margin:.2f}"

TOOLTIP_EXPECTED = "<b>number:</b> {number}<br><b>occurrences[%]:</b> {percentage:.2f}"

MATCHED_MSG = "<br><span style='color: green'><b>Data Matches</b></span>"


def prepare_report_data(file_id):
    data = DumpFileData.objects.filter(file=file_id)
    if not data:
        return
    _len = len(data)
    number_occurences = {}
    for row in range(1, 10):
        number_occurences[row] = 0
    # row for 0 value
    chart_data = [[0, 0.0, '', 0.0, '']]
    for row in data:
        val = row.data[0]
        number_occurences[int(val)] += 1
    for number, occurence in number_occurences.items():
        computed_val = occurence/_len
        computed_percentage = computed_val*100
        expected_val = BENFORD_MAPPING[number]/100
        expected_percentage = BENFORD_MAPPING[number]
        margin = computed_percentage - expected_percentage
        _row = [number, computed_val]
        tooltip1 = TOOLTIP_ACTUAL.format(number=number, occurrences=occurence, percentage=computed_percentage,
                                         margin=margin)
        if check_if_match(margin):
            tooltip1 += MATCHED_MSG
        _row.append(TOOLTIP_CONTAINER.format(content=tooltip1))
        _row.append(expected_val)
        tooltip2 = TOOLTIP_EXPECTED.format(number=number, percentage=expected_percentage)
        if check_if_match(margin):
            tooltip2 += MATCHED_MSG
        _row.append(TOOLTIP_CONTAINER.format(content=tooltip2))
        chart_data.append(_row)
    return chart_data


def check_if_match(margin):
    if abs(margin) <= 0.5:
        return True
    else:
        return False
