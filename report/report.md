
---

# ASR Shootout — Bangalore Locality Names

## Task

The goal was to test different speech-to-text systems on a real-world problem: finding Bangalore locality names from Hindi/Hinglish phone conversations, like the kind used in blue-collar hiring platforms.

---

# Approach

We recorded 20 MP3 clips ourselves. Each clip contains a short Hindi/Hinglish sentence where the speaker naturally says a Bangalore locality name, like:

> “Main Koramangala mein rehta hoon”

The recordings were done in different conditions:

* quiet room
* TV noise
* fan noise
* traffic noise
* whispering
* fast speech

The main metric was **locality entity accuracy** — whether the model could correctly identify the locality name.

We used two matching levels:

* **Strict match:** very close spelling match
* **Fuzzy match:** allows small spelling mistakes

WER and CER were also calculated, but they were not the main focus because this task is more about finding locality names correctly.

---

# Models Tested

| Model                   | Type      | Backend        |
| ----------------------- | --------- | -------------- |
| Deepgram nova-3         | Cloud API | deepgram-sdk   |
| faster-whisper large-v3 | Local CPU | faster-whisper |
| Sarvam AI Saarika v2.5  | Cloud API | REST           |

**Why these models:** Deepgram was mandatory. For the second slot I chose Sarvam over Azure, Google, and AssemblyAI because it is India-built, explicitly targets Hindi and regional languages, and has a free tier suitable for evaluation. For the third slot I chose faster-whisper large-v3 running locally rather than the Whisper API — it runs offline, has zero marginal cost, and represents the open-source baseline any team could self-host.

---

# Methodology

The API models received raw MP3 files directly.

The local models received 16 kHz mono audio after processing with librosa.

Latency was measured using total wall-clock time per file, including API response time. Results were cached so that no file was processed twice.

For locality matching:

* model outputs in Devanagari were transliterated into simplified Latin text
* a sliding window search with Levenshtein distance was used to compare outputs with the canonical locality names

Names already written in English, like “Koramangala” or “HSR Layout”, were used directly.

---

# Results

| Model            | WER†  | Strict locality | Fuzzy locality | Latency p50 | Latency p95 |
| ---------------- | ----- | --------------- | -------------- | ----------- | ----------- |
| Deepgram nova-3  | 1.39  | 15.8%           | 68.4%          | 1,994 ms    | 2,490 ms    |
| Sarvam Saarika   | 1.93  | 10.0%           | 60.0%          | 547 ms      | 793 ms      |
| Whisper large-v3 | 1.65  | 15.8%           | 68.4%          | 20,897 ms   | 24,104 ms   |

†WER values above 1.0 are a known artefact — WER counts insertions, so a transcript with more words than the reference can exceed 1.0 even with partial correctness. More importantly, script mixing (models outputting Devanagari while ground truth contains Latin words) causes systematic inflation. Locality accuracy is the operative metric for this task.

Deepgram and Whisper achieved the same accuracy scores.

Sarvam was:

* 3.6× faster than Deepgram
* 38× faster than Whisper at p50 latency

This speed difference is very important for real-time applications.

The strict scores are lower mainly because transliteration is imperfect.
For example, if a model correctly outputs “कोरमंगला”, the transliteration step may still slightly change the spelling and reduce the strict score.

The fuzzy scores give a more realistic picture of whether the model actually understood the locality name.

Sarvam’s strict score is also affected because it converts English locality names into Devanagari, which is actually correct behaviour for a Hindi-focused model. Deepgram keeps many English words in Latin script, which helps it score better in strict matching.

So the metric itself also affects the results.

---

# Failure Analysis

The failures mainly fall into five categories.

## 1. English-origin locality names — mostly successful

Examples:

* Whitefield
* Electronic City
* Majestic

All three models recognised these names well because they already exist in English-heavy training data.

---

## 2. Hindi/Sanskrit-origin names — mostly recoverable

Examples:

* Koramangala
* Banashankari
* Marathahalli

The models usually produced outputs very close to the correct pronunciation.
Most of these were recovered successfully using fuzzy matching.

These cases can be improved further with a locality post-processing step.

---

## 3. Kannada-origin names — failed across all models

Examples:

* Hebbal
* Yelahanka
* Yeshwanthpur

None of the models handled these properly. Instead, they produced similar-sounding Hindi words.

| File         | Deepgram           | Sarvam                 | Whisper              |
| ------------ | ------------------ | ---------------------- | -------------------- |
| Hebbal       | "cable se airport" | "tebala se eyaraporta" | "khebala se eraputa" |
| Yeshwanthpur | "ya svampura"      | "yaha asvanapura"      | "yasvanapurda"       |

This looks more like a vocabulary problem than a model quality issue.

A locality post-processor would help much more here than switching ASR models.

---

## 4. Long compound locality names — truncated by all models

Example:

* Rajarajeshwarinagar

All three models shortened the name into partial outputs like:

> “raja rajesvara”

These names are too long and uncommon for the ASR systems.

A curated locality dictionary would solve this more effectively.

---

## 5. Whispered audio — dangerous silent failures

In one whispered audio clip for “Yelahanka”:

* Deepgram returned an empty string without any error
* Sarvam returned “ye lahamka ka”
* Whisper returned “yala hamka”

The empty response is actually worse than a wrong transcription because the downstream system cannot detect that something failed.

Production systems should explicitly handle empty outputs.

---

# Recommendation

## Recommended setup

**Use Sarvam as the main ASR system together with a locality post-processor.**

The latency advantage is very important for live voice applications.

* Sarvam: 547 ms p50
* Deepgram: 1,994 ms p50
* Whisper large-v3: 20,897 ms p50

Whisper large-v3 is too slow for real-time calls.

**Cost at scale:** At 10,000 calls/day × 30s average, Deepgram costs roughly $21.50/day ($0.0043/min). Sarvam's API pricing is comparable. Whisper carries zero API cost but requires a GPU in production — roughly $200–400/month for a small inference server. Below ~50,000 minutes/month the managed APIs win on total cost of ownership; above that, a self-hosted Whisper-class model becomes competitive.

The accuracy gap between Sarvam and Deepgram is smaller than it appears because part of it comes from transliteration and script differences in the evaluation metric.

In practice:

* both models fail on similar difficult locality names
* both perform well on simpler cases

Sarvam is also more aligned with Indian-language inputs.

---

## Highest ROI improvement

The biggest engineering improvement would be:

**A locality post-processor using fuzzy matching against a curated list of around 200 Bangalore localities.**

Using Levenshtein distance ≤ 3 would recover many failed outputs regardless of the ASR model.

Most errors were predictable and systematic, making them ideal for post-processing.

---

## Specific actions

* Do not use Whisper large-v3 for live real-time calls
* Use smaller/local Hindi models only for async or batch processing if needed
* Explicitly handle empty ASR outputs
* Retry or reprompt users instead of silently failing
---

# Limitations

* The dataset only contains 20 samples from a single speaker
* These results are directionally useful but not statistically strong
* A larger dataset with multiple speakers is needed before making procurement decisions

WER and CER should also be interpreted carefully because:

* the transcripts mix Hindi and English
* different scripts and transliteration styles affect the calculations

A WER above 1.0 does not mean the model is random or unusable.
It mainly shows that WER is not the best metric for this evaluation setup.

Also:

* the phone-call condition was simulated
* real phone calls contain compression artefacts and lower audio quality that were not fully reproduced here
