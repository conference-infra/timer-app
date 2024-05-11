def timer(request):
    tracks = request.path.split('/')
    while '' in tracks:
        tracks.remove('')
    if tracks[0] == 'timer':
        tracks = tracks[1:]

    end = request.GET.dict()['end'] if 'end' in request.GET else None
    url = request.GET.dict()['url'] if 'url' in request.GET else None
    late_color = request.GET.dict()['late'] if 'late' in request.GET else 'yellow'
    very_late_color = request.GET.dict()['very_late'] if 'very_late' in request.GET else 'orangeRed'
    session_color = request.GET.dict()['session'] if 'session' in request.GET else 'white'
    break_color = request.GET.dict()['break'] if 'break' in request.GET else 'white'
    session_back = request.GET.dict()['session_back'] if 'session_back' in request.GET else 'black'
    break_back = request.GET.dict()['break_back'] if 'break_back' in request.GET else 'green'

    if not url and not end:
        return render(
            request,
            'timer_dox.html', 
            {})

    show_hours = 'true' if ('h' in request.GET) or ('show_hours' in request.GET) else 'false'
    show_seconds = 'true' if ('s' in request.GET) or ('show_seconds' in request.GET) else 'false'

    if url:
        response = urllib.urlopen(url)
        json_data = response.read()
        try:
            json_str = json.loads(json_data)
        except ValueError as e:
            return render(
                request,
                'timer_dox.html', 
                {
                    'error_message': 'URL parameter failed to produce JSON data. [%s] for URL = <a href="%s">%s</a>' % (unicode(e), url, url)
                })

    if end:
        begin_time = datetime.datetime.now()
        json_data = '[{"begin":"%s","end":"%s"}]' % (begin_time.isoformat(), end)

    return render(
        request,
        'timer.html', 
        {
            "tracks" : json.dumps(tracks),
            "json_data" : json_data,
            "show_hours" : show_hours,
            "show_seconds" : show_seconds,
            "late_color": late_color,
            "very_late_color": very_late_color,
            "session_color": session_color,
            "break_color": break_color,
            "session_back": session_back,
            "break_back": break_back
        })
