# Öğretim üyesi rehberi · Discrete Mathematics (YMT211) sitesi ve lab sistemi

Bu belge yalnızca size yönelik bakım notudur (öğrenciler siteyi görür, bu dosyayı değil).
Site: `https://drferhatu.github.io/discrete-mathematics/` · Depo: `drferhatu/discrete-mathematics`

---

## 1. Genel mimari

| Parça | Nerede | Ne işe yarar |
|---|---|---|
| Ders sitesi | bu depo, GitHub Pages | Haftalar, lab talimatları, proje, duyurular (Astro + Tailwind + KaTeX + Pagefind) |
| Lab şablonları | `labs/templates/labNN/` → her biri org'da ayrı **template repo** | Öğrencinin başlangıç kodu, testler, `check.py`, keşif defteri |
| Autograder | `labs/autograders/labNN/tests.json` → Classroom 50 assignment ayarı | Her push'ta pytest çalışır, puan GitHub Release olarak yayımlanır |
| Classroom 50 | classroom50.org + `FiratUniversity-IJDP-SoftEng` org'u | Roster, ödev kabulü, öğrenci repoları, puan toplama (CSV) |
| Editör | GitHub Codespaces (öğrencinin kendi reposundan) | Tarayıcıda VS Code; `.devcontainer` pytest'i kurar |
| Gizli materyal | `private/` (**.gitignore'da**) | Proje fikir bankası, lab çözümleri. Asla GitHub'a gitmez |

Neden cs50.dev değil de Codespaces? cs50.dev de bir Codespace; kendi `GITHUB_TOKEN`'ıyla çalıştığı için org'daki özel lab
repolarına push etmek öğrenci için ek token ayarı gerektirir. Classroom 50'nin belgelediği yol (web'den kabul + Codespaces
veya `gh student` CLI) sorunsuz. cs50.dev sitede "alternatif / pratik ortamı" olarak geçiyor.

---

## 2. Bir kerelik kurulum (ilk labdan önce)

### 2.1 Siteyi yayımlamak

> Not: `drferhatu/discrete-mathematics` adı şu an geçen yılki `Discrete-Mathematics-LabSession1` deposuna
> **yönlendirme** (eski ad). Aynı adla yeni depo açınca bu yönlendirme biter; eski depo kendi adıyla durmaya devam eder.

```bash
cd ".../Courses/DiscreteMath"
gh repo create drferhatu/discrete-mathematics --public --source . --push
gh api -X POST repos/drferhatu/discrete-mathematics/pages -f build_type=workflow
```

Ardından her `git push` siteyi 2–3 dakikada yeniler (Actions → "Deploy to GitHub Pages").

### 2.2 Organizasyonu Classroom 50'ye hazırlamak

`FiratUniversity-IJDP-SoftEng` şu an **Free** planda. Classroom 50, **Team** planı gerektirir (özel repodan Pages vb.).
Öğretmenlere ücretsizdir:

1. https://education.github.com/teachers → öğretmen olarak başvurun (fucar@firat.edu.tr + kurum kimliği). Onay birkaç gün sürebilir.
2. Onaydan sonra Education benefits sayfasından org'u **GitHub Team**'e ücretsiz yükseltin.
3. https://classroom50.org → Sign in with GitHub → org'u seçin → **Set up organization** (bir kez; `classroom50` reposu ve servis token'ı oluşur).
   Kurulum org'un temel iznini "No permission" yapar; geçen yılın GitHub Classroom repoları etkilenmez ama öğrenciler birbirinin reposunu göremez hâle gelir (istenen durum).
4. **Create classroom** → kısa ad: `dm-2026` (sitedeki tüm komutlar bu adı kullanır; değiştirirseniz `content/data/course.json → classroom.slug`'ı da değiştirin).
5. **Roster → Invite**: 19 öğrencinin e-postalarını toplu ekleyin. GitHub her birine org daveti yollar.
6. Codespaces: org **Settings → Codespaces → General** → "Enable for all members" ve **ownership: user** seçin
   (Codespaces öğrencinin kişisel ücretsiz kotasından düşer; org'a fatura gelmez).

Actions dakikası: Team planında ayda 3.000 dk. 19 öğrenci × ~5 push × 2 dk ≈ haftada 190 dk; rahat yeter.
Gerekirse assignment'ı "Submission type: tagged commit" yapıp yalnızca `gh student submit` ile notlandırabilirsiniz.

### 2.3 Lab 1'i açmak (Pazartesiden önce)

```bash
cd ".../Courses/DiscreteMath"
/opt/miniconda3/envs/ferhat_ml/bin/python scripts/verify_lab.py lab01      # boş şablon 0/21, çözüm 21/21 olmalı
scripts/publish_lab_template.sh lab01                                        # org'da özel template repo oluşturur
```

Sonra classroom50.org → `dm-2026` → **New assignment**:

- Slug: `lab01` · Name: `Lab 1 · Truth-Table Engine` · Type: Individual
- Template: `FiratUniversity-IJDP-SoftEng/dm-2026-lab01-template`
- Grading: **Autograded** · Submission type: **Every push** · Due: 4 Ekim 23:59
- Autograding tests: `labs/autograders/lab01/tests.json` içeriği (tek pytest testi, 10 puan)
- Kaydedin, **accept link**'i kopyalayın → `content/labs/lab-01.mdx` içindeki `acceptUrl: ""` alanına yapıştırıp push edin (boş kalırsa buton classroom50.org'a gider).

**Mutlaka bir test öğrenci hesabıyla deneyin**: kabul → Codespace → `python check.py` → push → Releases'ta puan.

---

## 2b. B planı: Classroom 50 olmadan (Lab 1'de kullanılıyor)

Lab sayfasında `mode: template` yazıyorsa öğrenciler şu yolu izler: public şablondan kendi hesabında **özel**
`dm-2026-labNN` deposunu açar, `drferhatu`'yu collaborator ekler, README'ye ad/numara yazar, push eder.
Şablondaki `.github/workflows/check.yml` her push'ta testleri öğrencinin reposunda çalıştırır (✅/❌).
Org içindeki (Classroom 50) repolarda bu workflow kendini atlar.

Hazırlık: `scripts/publish_lab_template.sh labNN --public`

Teslim tarihinden sonra, tek komut:

```bash
/opt/miniconda3/envs/ferhat_ml/bin/python scripts/collect_lab.py lab01 --due "2026-10-04 23:59"
```

- `dm-2026-lab01` adlı depoların bekleyen davetlerini kabul eder (başka davetlere dokunmaz).
- Her depoda teslim tarihinden önceki **son push**'u GitHub'ın workflow kaydından bulur (commit tarihi taklit edilebilir, bu edilemez).
- O commit'i klonlar, `tests/` klasörünü **resmi testlerle** değiştirir, pytest çalıştırır.
- 5 güne kadar geç push'lara günlük %10 kesinti uygular (`--late-days`).
- `private/grades/lab01.csv` yazar (GitHub'a gitmez): github, ad, numara, puan, teslim saati, not.

Öğrenci kodu sizin bilgisayarınızda (geçici klasörde, GitHub token'ı olmadan, zaman aşımıyla) çalışır.
Belirli depoları denemek için: `--repos kullanici/dm-2026-lab01`.

## 3. Haftalık akış

1. Hafta içeriği: `content/weeks/week-NN.md(x)` dosyasını düzenleyin; notlar bitince `status: ready`.
2. Yeni lab: `labs/templates/labNN/` (başlangıç kodu + `tests/` + `check.py` + README + `.devcontainer`), çözümü `private/solutions/labNN/`.
   Lab 1 klasörünü kopyalayıp başlamak en kolayı. Defter için `scripts/build_notebooks.py`'ye hücre listesi ekleyin.
3. `verify_lab.py labNN` → `publish_lab_template.sh labNN` → Classroom 50'de assignment.
4. `content/labs/lab-NN.md(x)`: `status: open`, `due`, `acceptUrl`; adımları Lab 1 sayfası gibi yazın.
5. Duyuru: `content/announcements/YYYY-MM-DD-ad.md` (`kind: info | important | exam | lab`, `pinned: true`).
6. Puanlar: submissions sayfasında **Collect now** → CSV indir.

Tarih/tatil/sınav: `content/data/schedule.json` (`status: normal | holiday | postponed | exam`). Final tarihi `finals.date`.

Yerel önizleme:

```bash
export PATH=/opt/homebrew/bin:$PATH
npm run dev          # http://localhost:4321/discrete-mathematics/
npm run build && /opt/miniconda3/envs/ferhat_ml/bin/python scripts/validate_content.py
```

---

## 4. Proje (%15 final)

- Fikir bankası: `private/project-ideas.md` (24 fikir, atama tablosu). Sitede yalnızca genel çerçeve var (`/project`).
- Atama: 4. hafta (12 Ekim) kişisel duyuru. Classroom 50'de şablonsuz, README'li bireysel `project` assignment açın
  ("Not graded" veya "Manual" notlandırma), her öğrenci kendi reposunda çalışır.
- Kilometre taşları sitede: H4 atama, H7 matematik tasarımı, H11 prototip, H15 demo günü.

---

## 5. Sık sorunlar

| Belirti | Neden / çözüm |
|---|---|
| Öğrenci "Not a member yet" görüyor | Org davetini kabul etmemiş ya da farklı GitHub hesabıyla girmiş. Roster'da e-postayı kontrol edin. |
| Accept 404 | Template özel ve assignment'ı bir **org owner** kaydetmedi. Assignment'ı açıp yeniden kaydedin. |
| Puan çıkmıyor | Öğrenci reposunda Actions sekmesi; kırmızıysa log'a bakın. Classroom 50'de "Collect now". |
| Codespace açılmıyor | Org Codespaces ayarı kapalı ya da öğrenci kotası dolmuş → cs50.dev veya yerel VS Code. |
