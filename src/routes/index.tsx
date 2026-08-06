import { createFileRoute } from "@tanstack/react-router";
import heroImage from "@/assets/streetlight-hero.jpg";

const TITLE = "Broken Streetlight Detection System";
const DESCRIPTION =
  "A beginner-friendly AI mini project that classifies nighttime streetlight images as Working or Broken using MobileNetV2, Streamlit and OpenCV.";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Broken Streetlight Detection System — AI Mini Project" },
      { name: "description", content: DESCRIPTION },
      { property: "og:title", content: TITLE },
      { property: "og:description", content: DESCRIPTION },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: Index,
});

const pages = [
  { icon: "🏠", name: "Home", detail: "Project title, description and a Start Detection button." },
  { icon: "📤", name: "Upload", detail: "Upload a JPG/JPEG/PNG image, preview it, then press Detect." },
  { icon: "📊", name: "Prediction", detail: "Image, prediction, confidence % — green for Working, red for Broken." },
  { icon: "ℹ️", name: "About", detail: "Problem statement, objectives, advantages, future scope, technologies." },
];

const tech = [
  ["Python", "Core language"],
  ["Streamlit", "Web interface"],
  ["TensorFlow / Keras", "Model training"],
  ["MobileNetV2", "Pre-trained CNN"],
  ["OpenCV", "Image processing"],
  ["NumPy", "Array maths"],
];

const files = [
  "streetlight_project/",
  "├── app.py                 # Streamlit app (Home, Upload, Prediction, About)",
  "├── requirements.txt",
  "├── README.md              # Overview, install, how to run, structure",
  "├── REPORT.md              # Abstract, methodology, conclusion, future scope",
  "├── model/train_model.py   # MobileNetV2 transfer learning",
  "├── dataset/Working/       # Your 'light is ON' images",
  "├── dataset/Broken/        # Your 'light is OFF' images",
  "├── utils/preprocess.py    # Resize + scale images",
  "├── utils/predict.py       # Load model, return label + confidence",
  "└── assets/",
];

function Index() {
  return (
    <main className="min-h-screen bg-background text-foreground">
      <section className="relative overflow-hidden">
        <img
          src={heroImage}
          alt="Nighttime street with one glowing streetlight and one dark broken streetlight"
          className="absolute inset-0 h-full w-full object-cover opacity-30"
        />
        <div
          className="relative px-6 py-20 sm:py-28"
          style={{ backgroundImage: "var(--gradient-hero)", opacity: 0.97 }}
        >
          <div className="mx-auto max-w-4xl text-center">
            <span className="inline-block rounded-full bg-primary-foreground/15 px-4 py-1 text-sm text-primary-foreground">
              💡 Beginner AI Mini Project
            </span>
            <h1 className="mt-5 text-4xl font-bold leading-tight text-primary-foreground sm:text-5xl">
              {TITLE}
            </h1>
            <p className="mx-auto mt-5 max-w-2xl text-base text-primary-foreground/85">
              Upload a nighttime streetlight photo and a pre-trained MobileNetV2 model
              predicts whether the lamp is <strong>Working</strong> or <strong>Broken</strong>,
              with a confidence percentage.
            </p>
            <div className="mt-8 flex flex-wrap justify-center gap-3">
              <code className="rounded-md bg-primary-foreground/15 px-4 py-2 text-sm text-primary-foreground">
                streamlit run app.py
              </code>
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-5xl px-6 py-16">
        <h2 className="text-2xl font-semibold">App pages</h2>
        <div className="mt-6 grid gap-4 sm:grid-cols-2">
          {pages.map((p) => (
            <div
              key={p.name}
              className="rounded-xl border border-border bg-card p-5"
              style={{ boxShadow: "var(--shadow-card)" }}
            >
              <p className="text-lg font-semibold">
                <span className="mr-2">{p.icon}</span>
                {p.name}
              </p>
              <p className="mt-2 text-sm text-muted-foreground">{p.detail}</p>
            </div>
          ))}
        </div>

        <div className="mt-10 grid gap-4 sm:grid-cols-2">
          <div className="rounded-xl border border-success/30 bg-card p-5">
            <p className="text-xl font-bold text-success">🟢 Working Streetlight</p>
            <p className="mt-1 text-sm text-muted-foreground">Shown in green with confidence, e.g. 94.2%</p>
          </div>
          <div className="rounded-xl border border-danger/30 bg-card p-5">
            <p className="text-xl font-bold text-danger">🔴 Broken Streetlight</p>
            <p className="mt-1 text-sm text-muted-foreground">Shown in red with confidence, e.g. 91.7%</p>
          </div>
        </div>
      </section>

      <section className="bg-secondary px-6 py-16">
        <div className="mx-auto max-w-5xl">
          <h2 className="text-2xl font-semibold">Technologies used</h2>
          <div className="mt-6 grid gap-3 sm:grid-cols-3">
            {tech.map(([name, role]) => (
              <div key={name} className="rounded-lg border border-border bg-card px-4 py-3">
                <p className="font-medium">{name}</p>
                <p className="text-sm text-muted-foreground">{role}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-5xl px-6 py-16">
        <h2 className="text-2xl font-semibold">Folder structure</h2>
        <pre className="mt-6 overflow-x-auto rounded-xl border border-border bg-card p-5 text-xs leading-6 text-muted-foreground">
          {files.join("\n")}
        </pre>

        <h2 className="mt-12 text-2xl font-semibold">How to run</h2>
        <ol className="mt-4 list-decimal space-y-2 pl-5 text-sm text-muted-foreground">
          <li>
            <code className="text-foreground">cd streetlight_project</code>
          </li>
          <li>
            <code className="text-foreground">pip install -r requirements.txt</code>
          </li>
          <li>
            Add your images to <code className="text-foreground">dataset/Working/</code> and{" "}
            <code className="text-foreground">dataset/Broken/</code>, then run{" "}
            <code className="text-foreground">python model/train_model.py</code>
          </li>
          <li>
            <code className="text-foreground">streamlit run app.py</code>
          </li>
        </ol>
        <p className="mt-4 text-sm text-muted-foreground">
          Without a trained model file the app still runs in a simple demo mode, so you can
          test the interface first.
        </p>
      </section>
    </main>
  );
}
