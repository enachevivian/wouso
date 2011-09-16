import os.path
from django.db import models
from django.conf import settings

class Group(models.Model):
    """ A group of artifacts for a Species. It cannot contain two artifacts of the same name."""
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name
    
class Artifact(models.Model):
    """ The generic artifact model. This should contain the name (identifier) and group,
    but also personalization such as: image (icon) and title
    """
    class Meta:
        unique_together = ('name', 'group')
    name = models.CharField(max_length=64) # level-1, quest-bun, etc
    title = models.CharField(max_length=100) # Maturator
    image = models.ImageField(upload_to=settings.MEDIA_ARTIFACTS_DIR, blank=True, null=True)
    group = models.ForeignKey(Group)
    
    @property
    def path(self):
        """ Image can be stored inside uploads or in theme, return the
        full path or the css class. """
        if self.image:
            return "%s/%s" % (settings.MEDIA_ARTIFACTS_URL, os.path.basename(str(self.image)))
        return "%s-%s" %  (self.group.name.lower(), self.name)
    
    @classmethod
    def get_level_1(kls):
        """ Temporary method for setting default artifact until God and Guildes """
        # TODO: I think this is deprecated
        try:
            return Artifact.objects.get(name='level-1')
        except:
            return None
    
    def __unicode__(self):
        return u"%s [%s]" % (self.name, self.group.name)
