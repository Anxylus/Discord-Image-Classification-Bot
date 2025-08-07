import discord
from discord.ext import commands
from mycode import gen_pass
import random, os
from model import get_class


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def generate_password(ctx):
    await ctx.send('Here is your password:')
    await ctx.send(gen_pass(10))

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)


@bot.command()
async def pangkatkan(ctx):
    await ctx.send('Masukkan dua angka yang ingin dipangkatkan')
    angka = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    angka = int(angka.content)
    
    await ctx.send('berikut pangkat dua dari {angka}')
    await ctx.send(angka ** 2)

@bot.command() 
async def help_me(ctx):
    list_command = {
        '$hello: Menyapa bot',
        '$heh: Mengulang kata "he" sebanyak yang diinginkan',
        '$generate_password: Menghasilkan password',
        '$pangkatkan: Menghitung pangkat dua dari angka yang diinput'
    }
    
    for i in list_command:
        await ctx.send(f'{i} : {list_command[i]}')

@bot.command()
async def send_meme(ctx):
    folder = os.listdir('gambar_meme')
    img = random.choice(folder)
    direktori = f'gambar_meme/{img}'
    with open(direktori, 'rb') as f:
        picture = discord.File(f)
    
    await ctx.send(file=picture)
        
@bot.command()
async def classify(ctx):
    if ctx.message.attachments:
        for file in ctx.message.attachments:
            file_name = file.filename
            file_url = file.url
            await file.save(f'./{file_name}')
            await ctx.send(f'File {file_name} telah diunggah. Memulai klasifikasi...')
            await ctx.send(f'Klasifikasi untuk {file_name} dimulai...')
            await ctx.send('Proses klasifikasi sedang berlangsung...')
            await ctx.send(f'File dapat diakses melalui {file_url}')
        
            kelas, skor = get_class('keras_model.h5', 'labels.txt', f'./{file.filename}')

            #Interferensi
            if kelas == 'Motherboard' and skor >= 0.7:
                await ctx.send(f'Gambar {file_name} diklasifikasikan sebagai {kelas} dengan skor kepercayaan {skor:.2f}.')
                await ctx.send('Motherboard adalah papan tempat semua komponen bersatu. Di sinilah CPU, GPU, RAM, dan storage saling terhubung dan berkomunikasi.')
                await ctx.send('Meski terlihat sederhana, perannya sangat vital karena tanpa motherboard, semua komponen lain tidak akan bisa saling berbicara.')
                await ctx.send('Ia adalah fondasi utama dari seluruh sistem.')

            elif kelas == 'CPU (Central Prosessing Unit)' and skor >= 0.7:
                await ctx.send(f'Gambar {file_name} diklasifikasikan sebagai {kelas} dengan skor kepercayaan {skor:.2f}.')
                await ctx.send('CPU adalah pusat kendali utama dari sebuah PC. Dialah yang memproses perintah, menjalankan logika, dan menghitung semua yang kamu lakukan.')
                await ctx.send('Ibarat jenderal yang memimpin seluruh pasukan, CPU memastikan semuanya berjalan dengan cepat dan efisien.')
                await ctx.send('Contoh keren: Intel Core i9 atau AMD Ryzen 9, kecepatan dan kekuatannya bikin kagum.')

            elif kelas == 'RAM (Random Access Memory)' and skor >= 0.7:
                await ctx.send(f'Gambar {file_name} diklasifikasikan sebagai {kelas} dengan skor kepercayaan {skor:.2f}.')
                await ctx.send('RAM adalah tempat semua proses aktif berlangsung. Saat kamu membuka game, aplikasi, atau browser, semuanya disimpan sementara di sini agar bisa diakses secepat mungkin.')
                await ctx.send('Semakin besar kapasitas RAM, semakin banyak hal yang bisa kamu lakukan tanpa lag.')
                await ctx.send('RAM itu seperti kecepatan refleks bagi komputer kamu.')

            elif kelas == 'GPU (Graphics Processing Unit)' and skor >= 0.7:
                await ctx.send(f'Gambar {file_name} diklasifikasikan sebagai {kelas} dengan skor kepercayaan {skor:.2f}.')
                await ctx.send('GPU adalah komponen yang bertugas menghasilkan tampilan visual. Dialah yang membuat game terlihat realistis, video lancar, dan grafis 3D tampil memukau.')
                await ctx.send('Kalau CPU adalah otak, GPU adalah mata dan tangan yang menciptakan keindahan visual.')
                await ctx.send('Contoh keren: NVIDIA GeForce RTX atau AMD Radeon RX, siap tempur untuk gaming, editing, dan rendering berat.')

            else:
                await ctx.send("barang atau produk ini anomali dan tidak dikenali 🗿🙏🏻")

    else:
        await ctx.send('Mohon unggah file gambar untuk diklasifikasikan.')
        




bot.run("rawr")
