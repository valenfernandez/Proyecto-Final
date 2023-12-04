from django.shortcuts import render
from .forms import SetPasswordForm
from django.contrib.auth.decorators import login_required
from .forms import SetPasswordForm
from django.contrib import messages
from django.shortcuts import render, redirect


# Create your views here.
@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tu contraseña fue cambiada de forma exitosa")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'usuarios/cambiar_contraseña.html', {'form': form})