"""
Definition of models.
"""

import uuid

from django.db import models

from django.db.models import ForeignKey
from django.urls import reverse

class Player(models.Model):
    playerID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=20)
    secondName = models.CharField(max_length=20)
    role = models.CharField(max_length=20)
    birthDate = models.DateField(default='2019-01-01')
    height = models.IntegerField(default=180)
    numberOfGoals = models.IntegerField(default=0)
    def __str__(self):
        return self.name + " " + self.secondName + " " + self.role


class ShootersMatch(models.Model):
    playerID = models.ForeignKey(Player, on_delete=models.CASCADE)
    goals = models.IntegerField(default=0)

class ShooterRank(models.Model):
    playerID = models.ForeignKey(ShootersMatch, on_delete=models.CASCADE)


class TeamSquad(models.Model):
    name = models.CharField(max_length=20, default="")
    playerID = models.ForeignKey(Player, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    squad = ForeignKey(TeamSquad, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Match(models.Model):
    MatchID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name='team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name='team2')
    points = models.IntegerField(default=0,)
    points2 = models.IntegerField(default=0,)
    date = models.DateField(default='2019-01-01')
    shootersPerMatch = models.ForeignKey(ShootersMatch, on_delete=models.CASCADE)
    def __str__(self):
        return self.team1.name +" "+ self.team2.name


class Tournament(models.Model):
    stage = models.IntegerField
    startingDate = models.DateTimeField('Starting date')
    endingDate = models.DateTimeField('Ending date')
    winner = models.ForeignKey(Team, on_delete=models.CASCADE)

    BEFORE = 'BF'
    IN_PROGRESS = 'IP'
    PLAYED = 'PL'
    CANCELLED = 'CN'

    STATE_CHOICES = (
        (BEFORE, 'Before'),
        (IN_PROGRESS, 'In progress'),
        (PLAYED, 'Played'),
        (CANCELLED, 'Cancelled'),
    )
    stateChoice = models.CharField(max_length=2, choices=STATE_CHOICES, default=BEFORE)


class Stage(models.Model):
    name = models.CharField(max_length=80)
    listOfMatches = models.ManyToManyField(Match)#, on_delete=models.CASCADE)
    def __str__(self):
        return self.name+ " "+self.listOfMatches.team1.name + " " + self.listOfMatches.team2.name


