from flask import Flask, render_template, request, redirect, url_for, flash
import os
from data_models import db, User, Movie
import requests


app = Flask(__name__)
