from django.views.generic.base import TemplateView
from robo_rally.courses.models import Course

class PickMapView(TemplateView):
    template_name = 'courses/maplist.html'
    def get_context_data(self, **kwargs):
        maps=Course.objects.all().values(
            'name', 'length', 'difficulty', 'min_players', 'max_players', 'filename'
        ).order_by('name')
        return dict(maps=maps)

class ViewCourseView(TemplateView):
    template_name = 'courses/view.html'
    def get_context_data(self, **kwargs):
        course = Course.objects.filter(filename='courses/' + kwargs['url'])[0]
        tostr = lambda a: " ".join(",".join(map(str, x)) for x in a)
        return dict(
            course=course, numflags=len(course.flags),
            flags=tostr(course.flags), spawn=tostr(course.spawn)
        )
