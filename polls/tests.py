import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Questions

# Create your tests here.
class QuestionsModelTests(TestCase):
    def test_pub_recently_with_future_date(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_qn = Questions(p_date = time)
        
        self.assertIs(future_qn.was_pub_recently(),False)
        
        
    def test_pub_recently_with_recent_date(self):
        time = timezone.now() - datetime.timedelta(hours=23,minutes=59,seconds=59)
        recent_qn = Questions(p_date = time)
        self.assertIs(recent_qn.was_pub_recently(),True)
    
    def test_pub_recently_with_old_date(self):
        time = timezone.now() - datetime.timedelta(days=1,seconds=1)
        old_qn = Questions(p_date = time)
        self.assertIs(old_qn.was_pub_recently(),False)

def create_questions(Q_text,days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Questions.objects.create(Q_text=Q_text,p_date=time)

class QuestionIndexViesTest(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertEqual(response,'No polls are available.')
        self.assertEqual(response.context['latest_q_list'],[])
        
    def test_past_question(self):
        question = create_questions(Q_text = "past_question",days = -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_q_list'],[question])
        
        
    def test_future_question(self):
        create_questions(Q_text = "future_question",days = 30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response,'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_q_list'],[])
        
    def test_future_and_past_question(self):
        question = create_questions(Q_text="Past question.", days=-30)
        create_questions(Q_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_q_list'],[question],)
        
    def test_two_past_question(self):
        question1 = create_questions(Q_text="Past question 1.", days=-30)
        question2 = create_questions(Q_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_q_list'],[question2, question1],)