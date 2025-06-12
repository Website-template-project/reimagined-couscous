from django.shortcuts import render
from django.http import JsonResponse
from .models import Message
import redis
from kafka import KafkaProducer