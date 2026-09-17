<!--fig-header-->
<picture>
  <img alt="Kayra, @Kayra-ML. Python · Machine Learning · Data Science. Find the story hidden in the data." src="assets/header-dark.svg" width="100%">
</picture>
<!--/fig-header-->

## The habit

Most people start with the model. I start with the question the data is actually
answering — which is usually not the question anyone asked out loud.

A loss curve that goes down is not the same thing as a model that works.
A 95 % accuracy is not the same thing as a 95 % accurate model. I care about
what the metric is actually measuring, which cases it ignores, and what the
model does on the examples nobody included in the test set. That is the
part that breaks in production.

The result is slower to start and harder to fool. `ModelAudit` exists because I
wanted a framework that probes what a model *does* rather than trusts what it
*says it is*. The F1 telemetry platform exists because the naive approach
pulls a full race worth of data into memory and dies; this one doesn't.

I'm Kayra. Python is my first language and the ML and data space is where I spend
most of my time. For tooling — bots, CLIs, APIs — I write TypeScript or Go and
pick whichever one the problem is asking for. Most of those projects were built
with AI-assisted workflows, and I say that plainly because hiding it would be
dishonest and using a tool well is its own skill.

<!--fig-fields-->
<div align="center">

```
Activity :: Kayra-ML {
    focus       : Machine Learning · Data Science · Python
    stack       : NumPy · Pandas · Scikit-Learn · Matplotlib · MySQL
    also_writes : TypeScript · JavaScript · Go · C++ (basic)
    workflow    : AI-assisted for non-Python projects — stated plainly, not hidden
    next        : Deep Learning · PyTorch · Model Deployment
    motto       : "Find the story hidden in the data 📊"
}
```

</div>
<!--/fig-fields-->

<!--fig-calendar-->
<div align="center">

<img src="https://github-readme-streak-stats.herokuapp.com/?user=Kayra-ML&background=0D1117&border=00FF41&stroke=00FF41&ring=00FF41&fire=00FF41&currStreakNum=FFFFFF&sideNums=FFFFFF&currStreakLabel=00FF41&sideLabels=00FF41&dates=8B949E" alt="Contribution streak — days since first commit, current and longest run." width="90%" />

</div>
<!--/fig-calendar-->

## Things I've built

<!--projects-->
<table>
<tr>
<td width="50%" valign="top">

#### [ModelAudit](https://github.com/Kayra-ML/ModelAudit)
<sub>`Python` · LLM Forensics · Prompt Evaluation</sub>

An open-source framework for **LLM identity forensics**, persona
detection, and AI transparency verification. Feed it a model,
get back a behavioral profile instead of a self-report.

**The hardest part:** models will tell you whatever you want
to hear if you ask them directly. The interesting work is
designing probes that catch the gap between what the model
claims and what it does.

Pure Python. No magic.

</td>
<td width="50%" valign="top">

#### [RoveCode Plugins](https://github.com/Kayra-ML/RoveCode_plugins)
<sub>`TypeScript` · MCP Server · AI-assisted</sub>

A token-efficient, domain-aware MCP server with a deterministic
router across **11 plugins and 72 skills**.

**The hardest part:** the router. It has to dispatch a request
to exactly the right plugin without reading the entire skill
list on every call, which is what naive implementations do.
This one reads once, routes in O(1).

</td>
</tr>
<tr>
<td width="50%" valign="top">

#### [F1 Data Analysis](https://github.com/Kayra-ML/fast_f1_data)
<sub>`Python` · `FastAPI` · `PostgreSQL` · `React`</sub>

Formula 1 analytics platform processing telemetry, lap times,
and race strategies with **RAM-efficient SQL** queries.

The challenge is volume: F1 telemetry is dense and the naive
approach runs out of memory before the race finishes. This one
streams and aggregates at the database layer instead of
pulling everything into Python first.

</td>
<td width="50%" valign="top">

#### [Qbeat](https://github.com/Kayra-ML/Qbeat)
<sub>`Python` · `discord.py` · `Asyncio` · `Docker`</sub>

Multi-instance Discord music bot cluster using an
**orchestrator and worker architecture** for zero-lag playback.

Single-instance bots stall when multiple servers are active
at once and the queue is long. This one splits work across
workers that the orchestrator assigns on demand rather than
queueing everything behind one audio thread.

</td>
</tr>
<tr>
<td width="50%" valign="top">

#### [ZscriptBot](https://github.com/Kayra-ML/ZscriptBot)
<sub>`TypeScript` — 6 ⭐</sub>

Discord command bot. Modular by design: every command lives in
its own file so the project doesn't collapse into one giant
handler as it grows. TypeScript keeps the message types honest.

</td>
<td width="50%" valign="top">

#### [Rove\_cli](https://github.com/Kayra-ML/Rove_cli)
<sub>`Go` · MIT</sub>

A CLI tool — written while learning Go. First Go project; it is
here because it is real work, not because it is finished.
The day a more serious Go repository exists, this line updates.

</td>
</tr>
</table>
<!--/projects-->

<!--fig-langs-->
<div align="center">

<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=Kayra-ML&layout=compact&theme=github_dark&hide_border=true&title_color=00FF41&text_color=c9d1d9&bg_color=0d1117&langs_count=8" alt="Languages by bytes of source GitHub reports for each one." width="60%" />

</div>
<!--/fig-langs-->

## What this page is not telling you

Every profile shows its wins. Here is the other column, because a page without one
is a sales pitch.

- **The account is young.** It opened in 2026. The streak graph above is
  mostly empty for a reason, and it shows exactly where it stops being empty
  rather than cropping the year to look busier than it is.
- **Stars are not users.** A few repositories have stars. That mostly means the
  README was readable, not that anyone ran the thing in production. I have not
  done the work of getting any of this in front of someone who would.
- **ML is genuinely in progress.** `next_goals` in the block above is not
  decoration. Scikit-Learn I know well. PyTorch and deployment are actively
  next — not "someday" next.
- **The AI-assisted workflow is real.** Most of my non-Python projects were
  built with AI assistance. I say this in my `whoami` and I mean it. Using a
  tool well is a skill; hiding that you used it is not.
- **Some repositories are experiments, not products.** `Rove_cli` came out of
  learning Go. They are on the profile because they are real, not because they
  are finished.

## Now

- Going deeper into the ML fundamentals: not just fitting models but understanding
  why a given model is the right or wrong choice for a given problem, and what
  the evaluation metric is actually measuring.
- Reading about **Deep Learning**. Nothing public in PyTorch yet — it goes on
  this page the day there is a repository to point at.
- The featured project list above is not a final state. More coming.

## How this page is built

The streak and language figures above are pulled live from
[github-readme-streak-stats](https://github.com/DenverCoder1/github-readme-streak-stats)
and [github-readme-stats](https://github.com/anuraghazra/github-readme-stats) on every
page load. Nothing here is hand-typed or can quietly go stale — the numbers update
themselves.

The project descriptions are written by hand, once, and updated when the project
changes. That is intentional: a one-line auto-generated description tells you
the language and the star count. A paragraph tells you what the hard part was.

<details>
<summary><b>Türkçe</b></summary>

<br/>

Merhaba, ben **Kayra**. **Python**, **veri bilimi** ve **makine öğrenmesi** alanında
çalışıyorum — NumPy, Pandas, Scikit-Learn, Matplotlib, SQL.

Çoğu işimde ortak bir alışkanlık var: **modelden önce veriyi anlamayı tercih ederim.**
Bir leaderboard skoru çok az şey söyler. Confusion matrix, residualler, modelin
yanlış olduğu hâlde en çok emin olduğu durumlar — bunlar gerçek bir şey söyler.

Python dışındaki projelerimi büyük ölçüde AI destekli iş akışıyla yazdım ve bunu
açıkça söylüyorum, çünkü saklamak dürüstlük değil, iyi kullanmak ise ayrı bir beceri.

Yukarıdaki "What this page is not telling you" bölümü de aynı sebepten var: hesap
yeni, yıldızlar kullanıcı sayısı değil, ve ML hâlâ aktif olarak öğreniliyor.
Bunları saklamak yerine yazmak bana daha doğru geliyor.

</details>

## Reach me

**byildiz.codes@gmail.com** · [@Kayra-ML](https://github.com/Kayra-ML) · [kayra-ml.github.io](https://kayra-ml.github.io)

Open to interesting problems, especially anything involving data that hasn't been
looked at carefully yet.
