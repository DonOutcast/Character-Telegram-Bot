from rest_framework import generics
from .models import Doctor, Patient, Exercise
from .serializers import DoctorSerializer, PatientSerializer, ExerciseSerializer


class DoctorListCreateView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class DoctorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class PatientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class ExerciseListCreateView(generics.ListCreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer


class ExerciseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer


class ExerciseListByDoctorView(generics.ListAPIView):
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        doctor_id = self.kwargs['doctor_id']
        return Exercise.objects.filter(doctors__id=doctor_id)


class ExerciseListByPatientView(generics.ListAPIView):
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return Exercise.objects.filter(patients__id=patient_id)
