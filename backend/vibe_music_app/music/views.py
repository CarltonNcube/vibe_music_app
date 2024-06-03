import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required

# Deezer API key
API_KEY = '83488bb3d8mshef666d0690a738ap100919jsn5f2f918578ce'

def top_artists():
    url = "https://deezerdevs-deezer.p.rapidapi.com/genre"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "deezerdevs-deezer.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    response_data = response.json()

    artists_info = []

    if 'data' in response_data:
        for genre in response_data['data']:
            genre_id = genre['id']
            genre_url = f"https://deezerdevs-deezer.p.rapidapi.com/genre/{genre_id}/artists"
            genre_response = requests.get(genre_url, headers=headers)
            genre_artists = genre_response.json()

            if 'data' in genre_artists:
                for artist in genre_artists['data'][:10]:  # Fetch top 10 artists per genre
                    name = artist.get('name', 'No Name')
                    avatar_url = artist.get('picture_medium', 'No URL')
                    artist_id = artist.get('id', 'No ID')
                    artists_info.append((name, avatar_url, artist_id))
            if len(artists_info) >= 10:  # Limit to top 10 artists overall
                break

    return artists_info

def top_tracks():
    url = "https://deezerdevs-deezer.p.rapidapi.com/editorial/0"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "deezerdevs-deezer.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    track_details = []

    if 'tracks' in data:
        shortened_data = data['tracks']['data'][:18]

        for track in shortened_data:
            track_id = track['id']
            track_name = track['title']
            artist_name = track['artist']['name']
            cover_url = track['album']['cover_medium']

            track_details.append({
                'id': track_id,
                'name': track_name,
                'artist': artist_name,
                'cover_url': cover_url
            })

    return track_details

def get_track_image(track_id, track_name):
    track_url = f"https://deezerdevs-deezer.p.rapidapi.com/track/{track_id}"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "deezerdevs-deezer.p.rapidapi.com"
    }
    response = requests.get(track_url, headers=headers)
    data = response.json()
    return data.get('album', {}).get('cover_medium', '')

def music(request, pk):
    track_id = pk
    url = f"https://deezerdevs-deezer.p.rapidapi.com/track/{track_id}"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "deezerdevs-deezer.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        track_name = data.get("title")
        artist_name = data.get("artist", {}).get("name", "No artist found")
        audio_url = data.get("preview")
        duration_text = data.get("duration")
        track_image = get_track_image(track_id, track_name)

        context = {
            'track_name': track_name,
            'artist_name': artist_name,
            'audio_url': audio_url,
            'duration_text': duration_text,
            'track_image': track_image,
        }
        return render(request, 'music.html', context)

    return HttpResponse("Failed to fetch track metadata")

@login_required(login_url='login')
def index(request):
    artists_info = top_artists()
    top_track_list = top_tracks()

    first_six_tracks = top_track_list[:6]
    second_six_tracks = top_track_list[6:12]
    third_six_tracks = top_track_list[12:18]

    context = {
        'artists_info': artists_info,
        'first_six_tracks': first_six_tracks,
        'second_six_tracks': second_six_tracks,
        'third_six_tracks': third_six_tracks,
    }
    return render(request, 'index.html', context)

def search(request):
    if request.method == 'POST':
        search_query = request.POST['search_query']
        url = "https://deezerdevs-deezer.p.rapidapi.com/search"
        querystring = {"q": search_query}
        headers = {
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": "deezerdevs-deezer.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        track_list = []

        if response.status_code == 200:
            data = response.json()
            tracks = data["data"]

            for track in tracks:
                track_name = track["title"]
                artist_name = track["artist"]["name"]
                duration = track["duration"]
                track_id = track["id"]
                track_image = get_track_image(track_id, track_name)

                track_list.append({
                    'track_name': track_name,
                    'artist_name': artist_name,
                    'duration': duration,
                    'trackid': track_id,
                    'track_image': track_image,
                })

            context = {
                'search_results_count': len(tracks),
                'track_list': track_list,
            }

            return render(request, 'search.html', context)

    return render(request, 'search.html')

def profile(request, pk):
    artist_id = pk
    url = f"https://deezerdevs-deezer.p.rapidapi.com/artist/{artist_id}"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "deezerdevs-deezer.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        name = data["name"]
        monthly_listeners = data["nb_fan"]
        header_url = data["picture_xl"]

        top_tracks = []
        top_tracks_url = f"https://deezerdevs-deezer.p.rapidapi.com/artist/{artist_id}/top?limit=10"
        tracks_response = requests.get(top_tracks_url, headers=headers)
        tracks_data = tracks_response.json()

        if 'data' in tracks_data:
            for track in tracks_data['data']:
                track_id = track["id"]
                track_name = track["title"]
                track_image = get_track_image(track_id, track_name)

                track_info = {
                    "id": track["id"],
                    "name": track["title"],
                    "durationText": track["duration"],
                    "playCount": track["rank"],
                    "track_image": track_image
                }

                top_tracks.append(track_info)

        artist_data = {
            "name": name,
            "monthlyListeners": monthly_listeners,
            "headerUrl": header_url,
            "topTracks": top_tracks,
        }
    else:
        artist_data = {}

    return render(request, 'profile.html', artist_data)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')

    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect('/')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    else:
        return render(request, 'signup.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

