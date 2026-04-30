# LinkedIn Post — conservatory.ai

> Aşağıda 2 farklı versiyon var. Birini seç ya da karıştır. Her ikisi de doğal, samimi bir tonla yazıldı — robotik AI yazısı gibi durmuyor.

---

## VERSIYON 1 — Hikaye anlatımıyla (uzun, daha kişisel)

So I built something kind of weird, and I think a lot of you might find it interesting.

I've been obsessed with how singers find out what their voice "is." You know — soprano, mezzo, tenor, bass. The whole Fach system. Most people figure this out by spending years with a voice teacher who tells them, "yeah, you're a lyric soprano." But not everyone has access to that. And honestly, even if you do, it costs a lot of time and money to even get a reasonable answer.

So I made conservatory.ai.

You upload a recording (or record live in the browser), and it runs your voice through a whole stack of acoustic analysis — Praat algorithms for jitter and shimmer, librosa for pitch tracking, FFT for vibrato detection, formant analysis to look for the singer's formant. The kind of stuff that voice researchers and speech pathologists actually use.

Then it tells you:
→ Your range and tessitura (where your voice naturally sits)
→ Your likely Fach (out of 11 classical categories)
→ Where your passaggio probably is
→ How healthy your vocal folds sound (jitter/shimmer)
→ What kind of music actually suits your voice — both classical AND modern

That last part is the one I'm most proud of. If the analysis says you're a baritone, it doesn't just stop there. It tells you Frank Sinatra and Hozier are good references, suggests "Largo al factotum" if you want to go classical, and warns you not to push into tenor territory. It's the conversation a good vocal coach would have, except free and instant.

A few things I want to be honest about:
— This won't replace a real voice teacher. It can't hear timbre or weight the way a human can. I made sure the app says this clearly.
— Single recordings have limits. Tessitura really needs longer samples to be accurate.
— The "vocal health" indicators (jitter, shimmer) can flag problems, but they're not a medical diagnosis. If something looks off, see an ENT.

But within those limits — it works. I tested it on operatic recordings, on pop singers, on my own voice. The classifications are reasonable. The recommendations are useful.

It supports 15 languages (Turkish, English, Chinese, Hindi, Spanish, Arabic, French, Bengali, Portuguese, Russian, Urdu, Indonesian, German, Japanese, Korean) because I wanted singers anywhere to be able to use it.

Tech stack for those curious: Flask backend, Praat-parselmouth + librosa for analysis, vanilla JS frontend (no React — wanted it lightweight), Chart.js for the pitch contour visualization.

If you sing, or you teach singing, or you're just curious what your voice looks like under a spectrogram — give it a try. Would love feedback on what's missing or what could be better.

🎼 [link]

#VocalAnalysis #MusicTech #OpenSource #Python #Flask #Singing #VoiceTraining #BuildInPublic

---

## VERSIYON 2 — Daha kısa, doğrudan

I built a thing this weekend(ish) and it's live.

It's called conservatory.ai. You give it a recording of you singing — even just 15 seconds of vocalises — and it tells you:

— What your voice type probably is (out of 11 classical categories)
— Your range, tessitura, passaggio
— Whether your vocal vibrato is healthy or wobbly
— What jitter and shimmer say about your vocal fold health
— Most importantly: what kind of music your voice is actually suited for. Both opera arias and modern stuff. So if you're a mezzo, it'll point you toward Carmen's "Habanera" AND Adele.

It uses Praat (the gold standard for acoustic phonetics) under the hood, plus librosa for pitch tracking. Same kind of analysis that voice researchers use, except wrapped in a UI that doesn't require a PhD to read.

15 language support, dark editorial design, free to use.

I'm not claiming it replaces a vocal coach. It can't hear what a trained ear hears. But for everyone who's ever wondered "wait, am I really a soprano?" and didn't have $80/hour to find out — it's a starting point.

Open to feedback. Especially harsh feedback.

🔗 [link]

#MusicTech #OpenSource #Python #VoiceAnalysis #SingingTeachers

---

## Hangisini Seçmeli?

**Versiyon 1** (uzun, hikaye): 
- Eğer takipçilerin senin yolculuğunu/projeni okumayı seviyorsa
- Build-in-public topluluğuna mesaj veriyorsan
- Music tech / vokal eğitim çevresine ulaşmak istiyorsan

**Versiyon 2** (kısa, doğrudan):
- Daha geniş kitle, daha az zaman okuyacak insanlar
- Tech-focused bağlantıların ağırlıkta
- Daha çabuk feedback istiyorsan

---

## 💡 Ek İpuçları

1. **Görsel ekle**: Pitch contour ekran görüntüsü veya repertuvar bölümünün ekran görüntüsü çok dikkat çeker.

2. **Yorum sorusu**: Postun en altına şöyle bir şey ekleyebilirsin:  
   *"Singers in my network — what's the one feature you'd want to see added?"*  
   Bu, etkileşimi artırır.

3. **İlk 10-30 dakika**: Yayınlandıktan sonra ilk yarım saat içinde gelen yorumları cevapla. LinkedIn algoritması bunu seviyor.

4. **Hashtag stratejisi**: 3-5 hashtag yeter, 10+ olursa spammy görünür.

5. **Yayın saati** (Türkiye saati): Salı-Perşembe, **09:00-11:00** arası en yüksek etkileşim.

İyi paylaşımlar! 🎼
