from django import forms

class CommentForm(forms.Form):
    # 评论 的 地方, id和type隐藏
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content_type = forms.CharField(widget=forms.HiddenInput)
    text = forms.CharField(widget=forms.Textarea)
