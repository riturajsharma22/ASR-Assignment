# Failure Analysis

Sections appear for every *(file, model)* pair where strict locality match failed. The side-by-side table covers **all** models for context.

---

## `01_koramangala_quiet.mp3` — model: `deepgram` — condition: quiet — [WRONG OUTPUT]

**Ground Truth:** Haan main Koramangala mein rehta hoon

**Canonical Locality:** `Koramangala`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | हां भाई. मैं कोरा मंगला में रहता हूं. | 3 |
| `sarvam` | हां भाई, मैं कोरामंगला में रहता हूं। | 1 |
| `whisper` | हाँ भाई मैं कोरा मंगला में रहता हूँ | 3 |

---

## `01_koramangala_quiet.mp3` — model: `whisper` — condition: quiet — [WRONG OUTPUT]

**Ground Truth:** Haan main Koramangala mein rehta hoon

**Canonical Locality:** `Koramangala`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | हां भाई. मैं कोरा मंगला में रहता हूं. | 3 |
| `sarvam` | हां भाई, मैं कोरामंगला में रहता हूं। | 1 |
| `whisper` | हाँ भाई मैं कोरा मंगला में रहता हूँ | 3 |

---

## `02_indiranagar_quiet.mp3` — model: `deepgram` — condition: quiet — [WRONG OUTPUT]

**Ground Truth:** Main Indiranagar side rehta hoon

**Canonical Locality:** `Indiranagar`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | मेरा घर इंदिरा नगर side है. | 3 |
| `sarvam` | मेरा घर इंदिरानगर साइड है | 1 |
| `whisper` | मेरा घर इंदिरा नगर साइड है | 3 |

---

## `02_indiranagar_quiet.mp3` — model: `whisper` — condition: quiet — [WRONG OUTPUT]

**Ground Truth:** Main Indiranagar side rehta hoon

**Canonical Locality:** `Indiranagar`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | मेरा घर इंदिरा नगर side है. | 3 |
| `sarvam` | मेरा घर इंदिरानगर साइड है | 1 |
| `whisper` | मेरा घर इंदिरा नगर साइड है | 3 |

---

## `03_whitefield_quiet.mp3` — model: `sarvam` — condition: quiet — [WRONG OUTPUT]

**Ground Truth:** Main Whitefield ke paas room leke rehta hoon

**Canonical Locality:** `Whitefield`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | मैं Whitefield के पास room लेकर रहता हूं. | 0 |
| `sarvam` | मैं वाइटफील्ड के पास रूम लेके रहता हूं। | 6 |
| `whisper` | मैं वाइट फिल्ड के पास रूम लेके रहता हूँ | 7 |

---

## `03_whitefield_quiet.mp3` — model: `whisper` — condition: quiet — [WRONG OUTPUT]

**Ground Truth:** Main Whitefield ke paas room leke rehta hoon

**Canonical Locality:** `Whitefield`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | मैं Whitefield के पास room लेकर रहता हूं. | 0 |
| `sarvam` | मैं वाइटफील्ड के पास रूम लेके रहता हूं। | 6 |
| `whisper` | मैं वाइट फिल्ड के पास रूम लेके रहता हूँ | 7 |

---

## `04_electroniccity_fast.mp3` — model: `sarvam` — condition: fast — [WRONG OUTPUT]

**Ground Truth:** Electronic City se bol raha hoon

**Canonical Locality:** `Electronic City`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | Electronic City से बोल रहा हूँ. | 0 |
| `sarvam` | इलेक्ट्रॉनिक सिटी से बोल रहा हूं। | 8 |
| `whisper` | Electronic City से बोल रहा हूँ | 0 |

---

## `05_marathahalli_quiet.mp3` — model: `deepgram` — condition: quiet — [WRONG OUTPUT]

**Ground Truth:** Meri job Marathahalli mein hai

**Canonical Locality:** `Marathahalli`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | मेरी job मराठा हल्ली में है. | 2 |
| `sarvam` | मेरी जॉब मराठा हल्ली में है। | 2 |
| `whisper` | मेरी जॉब मराठा हल्ली में है | 2 |

---

## `05_marathahalli_quiet.mp3` — model: `sarvam` — condition: quiet — [WRONG OUTPUT]

**Ground Truth:** Meri job Marathahalli mein hai

**Canonical Locality:** `Marathahalli`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | मेरी job मराठा हल्ली में है. | 2 |
| `sarvam` | मेरी जॉब मराठा हल्ली में है। | 2 |
| `whisper` | मेरी जॉब मराठा हल्ली में है | 2 |

---

## `05_marathahalli_quiet.mp3` — model: `whisper` — condition: quiet — [WRONG OUTPUT]

**Ground Truth:** Meri job Marathahalli mein hai

**Canonical Locality:** `Marathahalli`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | मेरी job मराठा हल्ली में है. | 2 |
| `sarvam` | मेरी जॉब मराठा हल्ली में है। | 2 |
| `whisper` | मेरी जॉब मराठा हल्ली में है | 2 |

---

## `06_hsrlayout_fan.mp3` — model: `deepgram` — condition: fan_noise — [WRONG OUTPUT]

**Ground Truth:** Roz HSR Layout travel karna padta hai

**Canonical Locality:** `HSR Layout`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | रोज़ एचेसार लेआउट travel करना पड़ता है. | 6 |
| `sarvam` | रोज़ एच एस आर लेआउट ट्रेवल करना पड़ता है। | 6 |
| `whisper` | *NO OUTPUT* | — |

---

## `06_hsrlayout_fan.mp3` — model: `sarvam` — condition: fan_noise — [WRONG OUTPUT]

**Ground Truth:** Roz HSR Layout travel karna padta hai

**Canonical Locality:** `HSR Layout`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | रोज़ एचेसार लेआउट travel करना पड़ता है. | 6 |
| `sarvam` | रोज़ एच एस आर लेआउट ट्रेवल करना पड़ता है। | 6 |
| `whisper` | *NO OUTPUT* | — |

---

## `06_hsrlayout_fan.mp3` — model: `whisper` — condition: fan_noise — [NO OUTPUT]

**Failure mode: NO OUTPUT** — model returned an empty transcript.

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | रोज़ एचेसार लेआउट travel करना पड़ता है. | 6 |
| `sarvam` | रोज़ एच एस आर लेआउट ट्रेवल करना पड़ता है। | 6 |
| `whisper` | *NO OUTPUT* | — |

---

## `07_btmlayout_noise.mp3` — model: `deepgram` — condition: background_noise — [WRONG OUTPUT]

**Ground Truth:** BTM Layout mein interview dene gaya tha

**Canonical Locality:** `BTM Layout`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | बीटीएम लेआउट में interview देने गया था. | 6 |
| `sarvam` | बीटीएम लेआउट में इंटरव्यू देने गया था। | 6 |
| `whisper` | BTM Layout में Interview देने गया था | 0 |

---

## `07_btmlayout_noise.mp3` — model: `sarvam` — condition: background_noise — [WRONG OUTPUT]

**Ground Truth:** BTM Layout mein interview dene gaya tha

**Canonical Locality:** `BTM Layout`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | बीटीएम लेआउट में interview देने गया था. | 6 |
| `sarvam` | बीटीएम लेआउट में इंटरव्यू देने गया था। | 6 |
| `whisper` | BTM Layout में Interview देने गया था | 0 |

---

## `08_bellandur_tv.mp3` — model: `deepgram` — condition: tv_noise — [WRONG OUTPUT]

**Ground Truth:** Office Bellandur side padta hai

**Canonical Locality:** `Bellandur`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | Office बेलांडुर site पड़ता है. | 3 |
| `sarvam` | ऑफिस बेलांडूर साइट पड़ता है। | 3 |
| `whisper` | ओफिस बेलांडूर साइट पढ़ता है | 3 |

---

## `08_bellandur_tv.mp3` — model: `sarvam` — condition: tv_noise — [WRONG OUTPUT]

**Ground Truth:** Office Bellandur side padta hai

**Canonical Locality:** `Bellandur`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | Office बेलांडुर site पड़ता है. | 3 |
| `sarvam` | ऑफिस बेलांडूर साइट पड़ता है। | 3 |
| `whisper` | ओफिस बेलांडूर साइट पढ़ता है | 3 |

---

## `08_bellandur_tv.mp3` — model: `whisper` — condition: tv_noise — [WRONG OUTPUT]

**Ground Truth:** Office Bellandur side padta hai

**Canonical Locality:** `Bellandur`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | Office बेलांडुर site पड़ता है. | 3 |
| `sarvam` | ऑफिस बेलांडूर साइट पड़ता है। | 3 |
| `whisper` | ओफिस बेलांडूर साइट पढ़ता है | 3 |

---

## `09_silkboard_traffic.mp3` — model: `deepgram` — condition: traffic — [WRONG OUTPUT]

**Ground Truth:** Silk Board ke traffic mein phasa hua hoon

**Canonical Locality:** `Silk Board`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | सिल्कबोर्ड के traffic में फँसा हुआ हूँ. | 3 |
| `sarvam` | सिल्क बोर्ड के ट्रैफिक में फंसा हुआ हूं। | 2 |
| `whisper` | सिल्क बोर्ड के ट्रैफिक में फसा हुआ हूँ | 2 |

---

## `09_silkboard_traffic.mp3` — model: `sarvam` — condition: traffic — [WRONG OUTPUT]

**Ground Truth:** Silk Board ke traffic mein phasa hua hoon

**Canonical Locality:** `Silk Board`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | सिल्कबोर्ड के traffic में फँसा हुआ हूँ. | 3 |
| `sarvam` | सिल्क बोर्ड के ट्रैफिक में फंसा हुआ हूं। | 2 |
| `whisper` | सिल्क बोर्ड के ट्रैफिक में फसा हुआ हूँ | 2 |

---

## `09_silkboard_traffic.mp3` — model: `whisper` — condition: traffic — [WRONG OUTPUT]

**Ground Truth:** Silk Board ke traffic mein phasa hua hoon

**Canonical Locality:** `Silk Board`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | सिल्कबोर्ड के traffic में फँसा हुआ हूँ. | 3 |
| `sarvam` | सिल्क बोर्ड के ट्रैफिक में फंसा हुआ हूं। | 2 |
| `whisper` | सिल्क बोर्ड के ट्रैफिक में फसा हुआ हूँ | 2 |

---

## `10_hebbal_outdoor.mp3` — model: `deepgram` — condition: outdoor — [WRONG OUTPUT]

**Ground Truth:** Hebbal se airport ja raha tha

**Canonical Locality:** `Hebbal`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | Cable से airport जा रहा था. | 5 |
| `sarvam` | टेबल से एयरपोर्ट जा रहा था। | 3 |
| `whisper` | खेबल से एरपुट जा रहा था | 2 |

---

## `10_hebbal_outdoor.mp3` — model: `sarvam` — condition: outdoor — [WRONG OUTPUT]

**Ground Truth:** Hebbal se airport ja raha tha

**Canonical Locality:** `Hebbal`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | Cable से airport जा रहा था. | 5 |
| `sarvam` | टेबल से एयरपोर्ट जा रहा था। | 3 |
| `whisper` | खेबल से एरपुट जा रहा था | 2 |

---

## `10_hebbal_outdoor.mp3` — model: `whisper` — condition: outdoor — [WRONG OUTPUT]

**Ground Truth:** Hebbal se airport ja raha tha

**Canonical Locality:** `Hebbal`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | Cable से airport जा रहा था. | 5 |
| `sarvam` | टेबल से एयरपोर्ट जा रहा था। | 3 |
| `whisper` | खेबल से एरपुट जा रहा था | 2 |

---

## `11_krpuram_outdoor.mp3` — model: `deepgram` — condition: outdoor — [WRONG OUTPUT]

**Ground Truth:** KR Puram cross kar liya maine

**Canonical Locality:** `KR Puram`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | केआर पुरम cross कर लिया मैंने. | 2 |
| `sarvam` | केआरपुरम क्रॉस कर लिया मैंने। | 2 |
| `whisper` | के आरपुरम क्रॉस कर लिया मैंने | 2 |

---

## `11_krpuram_outdoor.mp3` — model: `sarvam` — condition: outdoor — [WRONG OUTPUT]

**Ground Truth:** KR Puram cross kar liya maine

**Canonical Locality:** `KR Puram`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | केआर पुरम cross कर लिया मैंने. | 2 |
| `sarvam` | केआरपुरम क्रॉस कर लिया मैंने। | 2 |
| `whisper` | के आरपुरम क्रॉस कर लिया मैंने | 2 |

---

## `11_krpuram_outdoor.mp3` — model: `whisper` — condition: outdoor — [WRONG OUTPUT]

**Ground Truth:** KR Puram cross kar liya maine

**Canonical Locality:** `KR Puram`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | केआर पुरम cross कर लिया मैंने. | 2 |
| `sarvam` | केआरपुरम क्रॉस कर लिया मैंने। | 2 |
| `whisper` | के आरपुरम क्रॉस कर लिया मैंने | 2 |

---

## `12_yelahanka_whisper.mp3` — model: `deepgram` — condition: whisper — [NO OUTPUT]

**Failure mode: NO OUTPUT** — model returned an empty transcript.

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | *NO OUTPUT* | — |
| `sarvam` | ये लाहंग का साइड एक रूम देख रहा हूं। | 4 |
| `whisper` | याला हंका साइड एक रूम देख रहा हूँ | 4 |

---

## `12_yelahanka_whisper.mp3` — model: `sarvam` — condition: whisper — [WRONG OUTPUT]

**Ground Truth:** Yelahanka side ek room dekh raha hoon

**Canonical Locality:** `Yelahanka`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | *NO OUTPUT* | — |
| `sarvam` | ये लाहंग का साइड एक रूम देख रहा हूं। | 4 |
| `whisper` | याला हंका साइड एक रूम देख रहा हूँ | 4 |

---

## `12_yelahanka_whisper.mp3` — model: `whisper` — condition: whisper — [WRONG OUTPUT]

**Ground Truth:** Yelahanka side ek room dekh raha hoon

**Canonical Locality:** `Yelahanka`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | *NO OUTPUT* | — |
| `sarvam` | ये लाहंग का साइड एक रूम देख रहा हूं। | 4 |
| `whisper` | याला हंका साइड एक रूम देख रहा हूँ | 4 |

---

## `13_banashankari_whisper.mp3` — model: `deepgram` — condition: whisper — [WRONG OUTPUT]

**Ground Truth:** Haan sir main Banashankari se bol raha hoon

**Canonical Locality:** `Banashankari`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | हां sir, मैं बानाशंकरी से बोल रहा हूं. | 3 |
| `sarvam` | हां सर, मैं बाला शंकर जी से बोल रहा हूं। | 5 |
| `whisper` | हाँ सर मैं बाना शंकरी से बोल रहा हूँ | 3 |

---

## `13_banashankari_whisper.mp3` — model: `sarvam` — condition: whisper — [WRONG OUTPUT]

**Ground Truth:** Haan sir main Banashankari se bol raha hoon

**Canonical Locality:** `Banashankari`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | हां sir, मैं बानाशंकरी से बोल रहा हूं. | 3 |
| `sarvam` | हां सर, मैं बाला शंकर जी से बोल रहा हूं। | 5 |
| `whisper` | हाँ सर मैं बाना शंकरी से बोल रहा हूँ | 3 |

---

## `13_banashankari_whisper.mp3` — model: `whisper` — condition: whisper — [WRONG OUTPUT]

**Ground Truth:** Haan sir main Banashankari se bol raha hoon

**Canonical Locality:** `Banashankari`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | हां sir, मैं बानाशंकरी से बोल रहा हूं. | 3 |
| `sarvam` | हां सर, मैं बाला शंकर जी से बोल रहा हूं। | 5 |
| `whisper` | हाँ सर मैं बाना शंकरी से बोल रहा हूँ | 3 |

---

## `14_peenya_phone.mp3` — model: `deepgram` — condition: phone_style — [WRONG OUTPUT]

**Ground Truth:** Peenya industrial area mein kaam karta hoon

**Canonical Locality:** `Peenya`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | पीनिया industrial area में काम करता हूँ. | 3 |
| `sarvam` | पेनिया इंडस्ट्रियल एरिया में काम करता हूं। | 2 |
| `whisper` | PNI Industrial Area में काम करता हूँ | 4 |

---

## `14_peenya_phone.mp3` — model: `sarvam` — condition: phone_style — [WRONG OUTPUT]

**Ground Truth:** Peenya industrial area mein kaam karta hoon

**Canonical Locality:** `Peenya`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | पीनिया industrial area में काम करता हूँ. | 3 |
| `sarvam` | पेनिया इंडस्ट्रियल एरिया में काम करता हूं। | 2 |
| `whisper` | PNI Industrial Area में काम करता हूँ | 4 |

---

## `14_peenya_phone.mp3` — model: `whisper` — condition: phone_style — [WRONG OUTPUT]

**Ground Truth:** Peenya industrial area mein kaam karta hoon

**Canonical Locality:** `Peenya`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | पीनिया industrial area में काम करता हूँ. | 3 |
| `sarvam` | पेनिया इंडस्ट्रियल एरिया में काम करता हूं। | 2 |
| `whisper` | PNI Industrial Area में काम करता हूँ | 4 |

---

## `15_majestic_phone.mp3` — model: `sarvam` — condition: phone_style — [WRONG OUTPUT]

**Ground Truth:** Main abhi Majestic aa raha hoon

**Canonical Locality:** `Majestic`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | मैं अभी majestic आ रहा हूं. | 0 |
| `sarvam` | मैं अभी मैजेस्टिक आ रहा हूं। | 2 |
| `whisper` | मैं अभी Majestic आ रहा हूँ | 0 |

---

## `16_sarjapur_fast.mp3` — model: `deepgram` — condition: fast — [WRONG OUTPUT]

**Ground Truth:** Main Sarjapur road side rehta hoon

**Canonical Locality:** `Sarjapur`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | मैं सरचपुर roadside रहता हूं. | 3 |
| `sarvam` | मैं सरहजपुर रोड साइड रहता हूं। | 3 |
| `whisper` | मैं सरचपूर रोड साइट रहता हूँ | 3 |

---

## `16_sarjapur_fast.mp3` — model: `sarvam` — condition: fast — [WRONG OUTPUT]

**Ground Truth:** Main Sarjapur road side rehta hoon

**Canonical Locality:** `Sarjapur`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | मैं सरचपुर roadside रहता हूं. | 3 |
| `sarvam` | मैं सरहजपुर रोड साइड रहता हूं। | 3 |
| `whisper` | मैं सरचपूर रोड साइट रहता हूँ | 3 |

---

## `16_sarjapur_fast.mp3` — model: `whisper` — condition: fast — [WRONG OUTPUT]

**Ground Truth:** Main Sarjapur road side rehta hoon

**Canonical Locality:** `Sarjapur`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | मैं सरचपुर roadside रहता हूं. | 3 |
| `sarvam` | मैं सरहजपुर रोड साइड रहता हूं। | 3 |
| `whisper` | मैं सरचपूर रोड साइट रहता हूँ | 3 |

---

## `17_yeshwanthpur_fast.mp3` — model: `deepgram` — condition: fast — [WRONG OUTPUT]

**Ground Truth:** Yeshwanthpur station ke paas hoon

**Canonical Locality:** `Yeshwanthpur`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | या श्वंपुर station के पास हूँ. | 8 |
| `sarvam` | यह अश्वनपुर स्टेशन के पास है। | 8 |
| `whisper` | याश्वनपूर्ड स्टेशन के पास हूँ | 7 |

---

## `17_yeshwanthpur_fast.mp3` — model: `sarvam` — condition: fast — [WRONG OUTPUT]

**Ground Truth:** Yeshwanthpur station ke paas hoon

**Canonical Locality:** `Yeshwanthpur`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | या श्वंपुर station के पास हूँ. | 8 |
| `sarvam` | यह अश्वनपुर स्टेशन के पास है। | 8 |
| `whisper` | याश्वनपूर्ड स्टेशन के पास हूँ | 7 |

---

## `17_yeshwanthpur_fast.mp3` — model: `whisper` — condition: fast — [WRONG OUTPUT]

**Ground Truth:** Yeshwanthpur station ke paas hoon

**Canonical Locality:** `Yeshwanthpur`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | या श्वंपुर station के पास हूँ. | 8 |
| `sarvam` | यह अश्वनपुर स्टेशन के पास है। | 8 |
| `whisper` | याश्वनपूर्ड स्टेशन के पास हूँ | 7 |

---

## `18_thanisandra_normal.mp3` — model: `deepgram` — condition: normal — [WRONG OUTPUT]

**Ground Truth:** Thanisandra mein delivery ka kaam karta hoon

**Canonical Locality:** `Thanisandra`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | थानी संड्र में delivery का काम करता हूँ. | 3 |
| `sarvam` | थानी संड्रा में डिलीवरी का काम करता हूं। | 3 |
| `whisper` | थानी संडर में डिलिवरी का काम करता हूँ | 3 |

---

## `18_thanisandra_normal.mp3` — model: `sarvam` — condition: normal — [WRONG OUTPUT]

**Ground Truth:** Thanisandra mein delivery ka kaam karta hoon

**Canonical Locality:** `Thanisandra`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | थानी संड्र में delivery का काम करता हूँ. | 3 |
| `sarvam` | थानी संड्रा में डिलीवरी का काम करता हूं। | 3 |
| `whisper` | थानी संडर में डिलिवरी का काम करता हूँ | 3 |

---

## `18_thanisandra_normal.mp3` — model: `whisper` — condition: normal — [WRONG OUTPUT]

**Ground Truth:** Thanisandra mein delivery ka kaam karta hoon

**Canonical Locality:** `Thanisandra`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | थानी संड्र में delivery का काम करता हूँ. | 3 |
| `sarvam` | थानी संड्रा में डिलीवरी का काम करता हूं। | 3 |
| `whisper` | थानी संडर में डिलिवरी का काम करता हूँ | 3 |

---

## `19_rajarajeshwarinagar_normal.mp3` — model: `deepgram` — condition: normal — [WRONG OUTPUT]

**Ground Truth:** Rajarajeshwarinagar mein mera permanent address hai

**Canonical Locality:** `Rajarajeshwarinagar`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | राजा राजेश्वर में मेरा permanent address है. | 9 |
| `sarvam` | राजा राजेश्वर में मेरा परमानेंट एड्रेस है। | 9 |
| `whisper` | राजा रजेश्वरा में मेरा परमनेंट एड्रेस है | 9 |

---

## `19_rajarajeshwarinagar_normal.mp3` — model: `sarvam` — condition: normal — [WRONG OUTPUT]

**Ground Truth:** Rajarajeshwarinagar mein mera permanent address hai

**Canonical Locality:** `Rajarajeshwarinagar`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | राजा राजेश्वर में मेरा permanent address है. | 9 |
| `sarvam` | राजा राजेश्वर में मेरा परमानेंट एड्रेस है। | 9 |
| `whisper` | राजा रजेश्वरा में मेरा परमनेंट एड्रेस है | 9 |

---

## `19_rajarajeshwarinagar_normal.mp3` — model: `whisper` — condition: normal — [WRONG OUTPUT]

**Ground Truth:** Rajarajeshwarinagar mein mera permanent address hai

**Canonical Locality:** `Rajarajeshwarinagar`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | राजा राजेश्वर में मेरा permanent address है. | 9 |
| `sarvam` | राजा राजेश्वर में मेरा परमानेंट एड्रेस है। | 9 |
| `whisper` | राजा रजेश्वरा में मेरा परमनेंट एड्रेस है | 9 |

---

## `20_kengeriupanagara_normal.mp3` — model: `deepgram` — condition: normal — [WRONG OUTPUT]

**Ground Truth:** Kengeri Upanagara side aana padega

**Canonical Locality:** `Kengeri Upanagara`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | केंगेरी ऊपर नगरा side आना पड़ेगा. | 6 |
| `sarvam` | कैंगेरी उपनगरा साइड आना पड़ेगा। | 3 |
| `whisper` | कैंगरी उपनगरा साइड आना पड़ेगा | 4 |

---

## `20_kengeriupanagara_normal.mp3` — model: `sarvam` — condition: normal — [WRONG OUTPUT]

**Ground Truth:** Kengeri Upanagara side aana padega

**Canonical Locality:** `Kengeri Upanagara`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | केंगेरी ऊपर नगरा side आना पड़ेगा. | 6 |
| `sarvam` | कैंगेरी उपनगरा साइड आना पड़ेगा। | 3 |
| `whisper` | कैंगरी उपनगरा साइड आना पड़ेगा | 4 |

---

## `20_kengeriupanagara_normal.mp3` — model: `whisper` — condition: normal — [WRONG OUTPUT]

**Ground Truth:** Kengeri Upanagara side aana padega

**Canonical Locality:** `Kengeri Upanagara`

| Model | Transcript | Edit Distance |
|-------|-----------|:---:|
| `deepgram` | केंगेरी ऊपर नगरा side आना पड़ेगा. | 6 |
| `sarvam` | कैंगेरी उपनगरा साइड आना पड़ेगा। | 3 |
| `whisper` | कैंगरी उपनगरा साइड आना पड़ेगा | 4 |

---

