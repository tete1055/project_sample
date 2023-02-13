import os
import time
from django.shortcuts import ProfileModifyForm
from accounts.models import CustomUser
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import pykakasi.kakasi as kakasi
from django.http import JsonResponse
from PIL import Image
import pyheif
import base64
import magic
kakasi = kakasi()

@login_required
def profile_modify(request):
    user = CustomUser.objects.get(id=request.user.id)
    initial_data = {
        'name': user.name,
        'username': user.username,
        'context': user.context,
        'email': user.email,
        'gender': user.gender,
    }
    form = ProfileModifyForm(
        initial=initial_data
    )
    if request.method == 'POST':
        if not 'profile_modify_submit' in request.POST:
            image = request.FILES['image']
            # HEICファイルの場合のみ、変換処理を実行
            if image.name.endswith('.heic') or image.name.endswith('.heif'):
                # pyheifでHEICファイルを読み込み
                heif_file = pyheif.read(image)
                # PILで画像を読み込み
                img = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw", heif_file.mode, heif_file.stride)
                # 画像をJPEG形式で保存
                img.save(image.name.replace('.heic', '.jpeg'), 'JPEG', optimize=True, quality=50)
                # 画像をbase64エンコード
                with open(image.name.replace('.heic', '.jpeg'), "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
                # base64エンコードした画像をJSON形式に変換
                data = {'change_image': encoded_string}
                # JSON形式のデータを送信
                return JsonResponse(data)
            else:
                print(magic.from_buffer(image.read(1024) , mime=True))
                mime_type = magic.from_buffer(image.read(1024) , mime=True)
                if mime_type == 'image/jpeg' or 'image/png':
                    data = {'image': '画像は正常です。'}
                    return JsonResponse(data)
                else:
                    error = {
                        'error': 'このファイルは選択できません。',
                    }
                return JsonResponse(error)
        if 'profile_modify_submit' in request.POST:
            print('開始します。')
            if request.FILES.get('image'):
                print('画像を取得')
                new_profile_image = request.FILES.get('image')
                if new_profile_image.name.endswith('.heic') or new_profile_image.name.endswith('.heif'):
                    print('画像形式を変更')
                    # pyheifでHEICファイルを読み込み
                    heif_file = pyheif.read(new_profile_image)
                    # PILで画像を読み込み
                    img = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw", heif_file.mode, heif_file.stride)
                    # 画像をJPEG形式で保存
                    converted_image_path = new_profile_image.name.replace('.heic', '.jpeg')
                    img.save(converted_image_path, 'JPEG', optimize=True, quality=50, upload_to='media/')
                    user.image = converted_image_path
                    user.name = request.POST['name']
                    user.username = request.POST['username']
                    user.context = request.POST['context']
                    user.email = request.POST['email']
                    user.gender = request.POST['gender']
                    user.save()
                else:
                    user.image = new_profile_image
                    user.name = request.POST['name']
                    user.username = request.POST['username']
                    user.context = request.POST['context']
                    user.email = request.POST['email']
                    user.gender = request.POST['gender']
                    user.save()
    params = {
        'login_user': request.user,
        'form': form,
        'user': user,
    }
    return render(request, 'profile_modify.html', params)