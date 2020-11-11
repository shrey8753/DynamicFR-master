import os

from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
import face_recognition
import cv2
import numpy as np
from django.utils import timezone

from project import settings
from . import models
# Create your views here.

base_dir =settings.MEDIA_ROOT

def home(request):

    if request.method == 'POST':
        try:
            entry = request.POST.get("first")
            entry = int(entry)
            return redirect('core:station_entry', entry)
        except:
            pass

        try:
            exit = request.POST.get("second")
            exit = int(exit)
            return redirect('core:station_exit', exit)
        except:
            pass
    return render(request, 'core/index.html')


def StationEntryView(request, station_no):

    if request.method == 'POST':
        try:
            entry = request.POST.get("first")
            entry = int(entry)
            return redirect('core:station_entry', entry)
        except:
            pass

        try:
            exit = request.POST.get("second")
            exit = int(exit)
            return redirect('core:station_exit', exit)
        except:
            pass
    station = models.Station.objects.get(station_no=station_no)
    pics = list(models.Person.objects.all().values_list('pic', flat=True))
    known_face_names = list(models.Person.objects.all().values_list('name', flat=True))
    uids = list(models.Person.objects.all().values_list('uid', flat=True))
    known_face_encodings = []
    for pic in pics:
        image = face_recognition.load_image_file(os.path.join(base_dir, str(pic)))
        image_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(image_encoding)

    i = 0

    video_capture = cv2.VideoCapture(0)
    face_locations = []
    face_encodings = []
    face_names = []
    face_uids = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        try:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # small_frame = frame

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                face_uids = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
                    name = "Unknown"
                    uid = -1
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        # print("pehchaan liya", name)
                        uid = uids[best_match_index]
                        person = models.Person.objects.get(uid=uid)
                        log = models.Log.objects.get_or_create(person=person, entry_station=station, status=0)
                    face_names.append(name)
                    face_uids.append(uid)
            i += 1
            process_this_frame = not process_this_frame

            # Display the results
            for (top, right, bottom, left), name, uid in zip(face_locations, face_names, face_uids):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, str(name + ':' + str(uid)), (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        except:
            # print(frame)
            pass
        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

    return render(request, 'core/index.html')


def StationExitView(request, station_no):
    if request.method == 'POST':
        try:
            entry = request.POST.get("first")
            entry = int(entry)
            return redirect('core:station_entry', entry)
        except:
            pass

        try:
            exit = request.POST.get("second")
            exit = int(exit)
            return redirect('core:station_exit', exit)
        except:
            pass
    station = models.Station.objects.get(station_no=station_no)
    pics = list(models.Person.objects.all().values_list('pic', flat=True))
    known_face_names = list(models.Person.objects.all().values_list('name', flat=True))
    uids = list(models.Person.objects.all().values_list('uid', flat=True))
    known_face_encodings = []
    for pic in pics:
        # print(pic)
        image = face_recognition.load_image_file(os.path.join(base_dir, str(pic)))
        image_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(image_encoding)

    i = 0

    video_capture = cv2.VideoCapture(0)
    face_locations = []
    face_encodings = []
    face_names = []
    face_uids = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        try:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                face_uids = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
                    name = "Unknown"
                    uid = -1
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        uid = uids[best_match_index]
                        person = models.Person.objects.get(name=name)
                        try:
                            log = models.Log.objects.get(person=person, status=0)
                            log.exit_station = station
                            log.exit_datetime = timezone.now()
                            log.status = 1
                            log.fare = 20
                            log.save()
                            try:
                                subject = 'Thanks for Travelling in Yugant Express'
                                message = person.name + ', thanks for travelling.\n From Station : {} \n Entry time : {} \n To station : {}\n Exit Time : {} \n Your Fare : {}'.format(
                                    log.entry_station, log.entry_datetime, log.exit_station, log.exit_datetime, log.fare)
                                from_email = settings.EMAIL_HOST_USER
                                to_email = [person.email]
                                email = EmailMessage(subject=subject, from_email=from_email, to=to_email, body=message)
                                email.send()
                                # print('email sent')
                            except:
                                # print('failed to send email')
                                pass
                        except:
                            # print('Chada hi nhi tha... cheating krta h yeh !! fine lo')
                            pass
                    # print(name)
                    face_names.append(name)
                    face_uids.append(uid)
            i += 1
            process_this_frame = not process_this_frame

            # Display the results
            for (top, right, bottom, left), name, uid in zip(face_locations, face_names, face_uids):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, str(name + ':'+ str(uid)), (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        except:
            # print("Cannot read frame")
            pass
        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

    return render(request, 'core/index.html')