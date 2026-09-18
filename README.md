<!--fig-header-->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
  <img alt="Burak, @Kayra-ML. Türkiye. I'd rather understand the data than chase the score." src="assets/header-light.svg" width="100%">
</picture>
<!--/fig-header-->

## The habit

A model giving a high score does not automatically mean it learned the right thing.

So before I care about accuracy, I care about the data.

I look at distributions, missing values, class balance, correlations, leakage,
outliers and the metric itself. Then I build the model.

Most of my work starts in **Python**.
**NumPy** handles the numbers, **Pandas** handles the data, **Scikit-learn**
handles most of the classical ML pipeline, and **Matplotlib** helps me see
what the numbers are trying to hide.

I am **Burak**, working under **@Kayra-ML** from Türkiye.

My main direction is **Machine Learning and data**, but I also build APIs,
developer tools, automation systems and AI-related projects when the problem
needs them.

I would rather understand why a model works than celebrate a benchmark number
I cannot explain.

<!--fig-fields-->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/fields-dark.svg">
  <img alt="Activity as a struct: machine learning, Python, repositories, current stack and next goals." src="assets/fields-light.svg" width="100%">
</picture>
<!--/fig-fields-->

<!--fig-calendar-->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/calendar-dark.svg">
  <img alt="The contribution year as a hexdump — one byte per day, shaded in Kayra green by contribution count." src="assets/calendar-light.svg" width="100%">
</picture>
<!--/fig-calendar-->

## Things I've built

<!--projects-->

<table>
<tr>
<td width="50%" valign="top">

#### [ModelAudit](https://github.com/Kayra-ML/ModelAudit)

<sub>`AI` · `LLM Forensics` · `Evaluation`</sub>

An open research project for analyzing the real behaviour and identity of
large language models.

Instead of trusting what a model says it is, the project looks at technical
and behavioural signals: response patterns, tokenizer behaviour, limits,
errors and other fingerprints.

**Interesting part:** self-report is not evidence.

The goal is to measure behaviour instead of trusting the label placed on
the model.

<sub>0x00 · AI / model evaluation</sub>

</td>
<td width="50%" valign="top">

#### [fast_f1_data](https://github.com/Kayra-ML/fast_f1_data)

<sub>`Python` · `FastAPI` · `PostgreSQL` · `Data Analysis`</sub>

A Formula 1 analytics platform built around telemetry, lap data and race
strategy analysis.

Instead of loading an entire race into Python memory and processing everything
there, the system pushes aggregation and filtering toward the database.

**Interesting part:** moving computation closer to the data.

Less memory usage, smaller responses and a cleaner path from raw telemetry to
useful analysis.

<sub>0x01 · Python / data systems</sub>

</td>
</tr>

<tr>
<td width="50%" valign="top">

#### [Qbeat](https://github.com/Kayra-ML/Qbeat)

<sub>`Python` · `asyncio` · `Discord` · `Docker`</sub>

A Discord music system designed around a cluster architecture.

One main bot handles commands while worker bots handle voice channels, allowing
multiple sessions to run without forcing everything through one process.

Supports YouTube, Spotify, SoundCloud, queues, volume control, slash commands,
Docker deployment and modular cogs.

**Interesting part:** distributing the workload instead of making one bot do
everything.

<sub>0x02 · distributed bot architecture</sub>

</td>
<td width="50%" valign="top">

#### [RoveCode_plugins](https://github.com/Kayra-ML/RoveCode_plugins)

<sub>`TypeScript` · `MCP` · `AI Agents`</sub>

A domain-aware plugin and skill system for AI agents.

The project is built around routing an incoming task to the correct tool or
skill without dumping the entire plugin catalogue into context every time.

**Interesting part:** tool routing.

Agent systems become expensive and noisy very quickly if every request begins
by reading every available skill.

<sub>0x03 · agent infrastructure</sub>

</td>
</tr>

<tr>
<td width="50%" valign="top">

#### [SearchForge_open](https://github.com/Kayra-ML/SearchForge_open)

<sub>`JavaScript` · `Search` · `Static Index`</sub>

Open-source search tooling built around a static search index.

The index can be generated once and queried directly from the client without
requiring a backend request for every search.

**Interesting part:** search without a permanently running search server.

<sub>0x04 · search systems</sub>

</td>
<td width="50%" valign="top">

#### [KeyLingo](https://github.com/Kayra-ML/KeyLingo)

<sub>`Python` · `Automation` · `Language Tools`</sub>

A small Python utility built around a simple idea: remove repetitive language
workflow from the keyboard.

It is intentionally focused.

**Interesting part:** some of the most useful programs are not platforms.
They are tools that remove one annoying repeated action.

<sub>0x05 · Python utility</sub>

</td>
</tr>

<tr>
<td width="50%" valign="top">

#### [Rove_cli](https://github.com/Kayra-ML/Rove_cli)

<sub>`Go` · `CLI`</sub>

A command-line project written while exploring Go and CLI architecture.

It is not here because Go is my main language.

It is here because learning a language makes more sense to me when there is a
real tool at the end of it.

<sub>0x06 · Go / CLI</sub>

</td>
<td width="50%" valign="top">

#### [pyutils-toolkit](https://github.com/Kayra-ML/pyutils-toolkit)

<sub>`Python` · `Utilities`</sub>

Python utilities that kept appearing across different projects, collected into
one place instead of being rewritten every time.

Not a product.

A toolbox.

<sub>0x07 · Python</sub>

</td>
</tr>
</table>
<!--/projects-->

<!--fig-segments-->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/segments-dark.svg">
  <img alt="Public projects shown as segments on a single timeline." src="assets/segments-light.svg" width="100%">
</picture>
<!--/fig-segments-->

<!--fig-langs-->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/langs-dark.svg">
  <img alt="Languages and tools represented as a memory map, with Python and the machine learning stack at the center." src="assets/langs-light.svg" width="100%">
</picture>
<!--/fig-langs-->

## The stack

The tools I currently spend most of my time with are:

`Python` · `NumPy` · `Pandas` · `Scikit-learn` · `Matplotlib`

Most of what I am studying and building around them falls into:

`Machine Learning` · `Data Analysis` · `Feature Engineering` ·
`Model Evaluation` · `Data Visualization`

I use notebooks when exploration matters and regular Python projects when the
work starts becoming a system.

The distinction matters.

A notebook is good for asking questions.

A project is better when the answer needs to keep running.

## What this page is not telling you

Every GitHub profile naturally shows its best side.

This is the other column.

* **Machine Learning is still an active learning process.**
  I am comfortable working with Python and the classical data stack, but I am
  still going deeper into the mathematics, algorithms and reasoning behind the
  models instead of pretending the roadmap is finished.

* **A certificate is not the same thing as understanding.**
  Completing a course or notebook means very little if I cannot explain what
  the model learned, why the metric changed, or what would break the result.

* **Python is clearly my main language.**
  I experiment with TypeScript, JavaScript and Go, but data work naturally
  keeps pulling me back toward Python.

* **Not every repository is a polished product.**
  Some are experiments, some are utilities and some exist because I needed to
  understand an idea by building it.

* **A good benchmark can still describe a bad model.**
  Data leakage, class imbalance or a badly selected metric can make a result
  look impressive without making it useful.

That is why I care increasingly less about whether a number looks good and more
about whether I can explain where it came from.

## Now

* Going deeper into **Machine Learning fundamentals** rather than only learning
  library calls.

* Working more seriously with **Scikit-learn pipelines, preprocessing,
  feature engineering, validation and model evaluation**.

* Using **NumPy and Pandas** less as syntax to memorize and more as tools for
  understanding and transforming real datasets.

* Improving how I visualize and explain results with **Matplotlib**.

* Moving toward **Deep Learning and PyTorch** after the classical ML foundation
  is strong enough.

* Building projects instead of collecting tutorials.

## How this page is built

The visual language of this profile is based around **Kayra green**.

Recommended primary color:

`#D7FF43`

with near-black backgrounds:

`#0D0D0D`

and softer green shades for lower-intensity data.

The figures live under `assets/` and are referenced through `<picture>` tags so
GitHub can show separate light and dark versions.

The activity calendar can be generated from GitHub contribution data, with one
cell for every day and the green intensity representing activity.

The language figure can use the actual amount of source code GitHub reports
instead of manually written percentages.

That means the profile can behave more like a visualization of the repository
than a static résumé.

<details>
<summary><b>Türkçe</b></summary>

<br/>

Merhaba, ben **Burak**. GitHub'da **@Kayra-ML** kullanıcı adını kullanıyorum.

Ana odağım **Machine Learning ve Python**.

Şu anda özellikle **NumPy, Pandas, Scikit-learn ve Matplotlib** üzerinde
çalışıyorum.

Machine Learning tarafında benim için önemli olan sadece bir modeli eğitip
yüksek accuracy görmek değil.

Önce verinin ne söylediğine bakmayı tercih ediyorum.

Eksik veriler, sınıf dağılımı, feature'lar, korelasyonlar, data leakage,
validation yöntemi ve kullanılan metriğin gerçekten ne ölçtüğü modelin
kendisinden bile daha önemli olabiliyor.

%97 accuracy görmek güzel olabilir.

Ama model sadece verinin %97'sini oluşturan sınıfı tahmin ediyorsa aslında hiçbir
şey öğrenmemiş de olabilir.

Bu yüzden Scikit-learn kullanırken yalnızca `.fit()` ve `.predict()` kısmıyla
ilgilenmek istemiyorum.

Modelin **neden** o sonucu verdiğini anlamak istiyorum.

GitHub profilimde ML projelerinin yanında botlar, API'ler, CLI araçları ve AI
altyapı projeleri de bulunuyor.

Çünkü öğrenmenin en iyi yollarından birinin gerçek bir şey üretmek olduğunu
düşünüyorum.

</details>

## Reach me

**[byildiz.codes@gmail.com](mailto:byildiz.codes@gmail.com)** · [@Kayra-ML](https://github.com/Kayra-ML) · [kayra-ml.github.io](https://kayra-ml.github.io)

Open to interesting problems involving **machine learning, data, AI systems and developer tools**.
