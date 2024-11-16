final int USER = 0;
final int FOURIER = 1;

ArrayList<PVector> drawing = new ArrayList<>();
ArrayList<PVector> path = new ArrayList<>();
Fourier[] fourierX, fourierY;
float time = 0;
int state = -1;

void setup() {
  size(800, 600);
  background(0);
  surface.setTitle("Draw anything :)");
  surface.setResizable(true);
  surface.setLocation(100, 100);
}

void mousePressed() {
  state = USER;
  drawing.clear();
  path.clear();
  time = 0;
}

void mouseReleased() {
  state = FOURIER;

  ArrayList<Float> x = new ArrayList<>();
  ArrayList<Float> y = new ArrayList<>();

  for (PVector p : drawing) {
    x.add(p.x);
    y.add(p.y);
  }

  fourierX = dft(toArray(x));
  fourierY = dft(toArray(y));

  System.out.println(fourierX.length);
  System.out.println(fourierY.length);
  
  // Sort by amplitude in descending order using a custom sort function
  sortByAmplitude(fourierX);
  sortByAmplitude(fourierY);
}

void draw() {
  background(55, 0, 20);

  if (state == USER) {
    stroke(255);
    strokeWeight(2);
    noFill();
    beginShape();
    for (PVector v : drawing) {
      vertex(v.x + width / 2, v.y + height / 2);
    }
    endShape();

    PVector point = new PVector(mouseX - width / 2, mouseY - height / 2);
    drawing.add(point);
  } else if (state == FOURIER) {
    PVector vx = epicycles(width / 2, 100, 0, fourierX);
    PVector vy = epicycles(100, height / 2, HALF_PI, fourierY);

    PVector v = new PVector(vx.x, vy.y);
    path.add(0, v);

    stroke(255);
    strokeWeight(2);
    line(vx.x, vx.y, v.x, v.y);
    line(vy.x, vy.y, v.x, v.y);

    beginShape();
    noFill();
    strokeWeight(2);
    for (PVector p : path) {
      vertex(p.x, p.y);
    }
    endShape();

    float dt = TWO_PI / fourierY.length;
    time += dt;

    if (time > TWO_PI) {
      time = 0;
      path.clear();
    }
  }
}

// Helper method to convert ArrayList<Float> to float[]
float[] toArray(ArrayList<Float> list) {
  float[] array = new float[list.size()];
  for (int i = 0; i < list.size(); i++) {
    array[i] = list.get(i);
  }
  return array;
}

PVector epicycles(float x, float y, float rotation, Fourier[] fourier) {
  for (int i = 0; i < fourier.length; i++) {
    float prevx = x;
    float prevy = y;

    float freq = fourier[i].freq;
    float radius = fourier[i].amp;
    float phase = fourier[i].phase;

    x += radius * cos(freq * time + phase + rotation);
    y += radius * sin(freq * time + phase + rotation);

    stroke(255, 100);
    noFill();
    ellipse(prevx, prevy, radius * 1.5, radius * 1.5);
    stroke(255);
    line(prevx, prevy, x, y);
  }

  return new PVector(x, y);
}

// Custom sort function to sort Fourier[] by amplitude
void sortByAmplitude(Fourier[] fourier) {
  for (int i = 0; i < fourier.length - 1; i++) {
    for (int j = i + 1; j < fourier.length; j++) {
      if (fourier[i].amp < fourier[j].amp) {
        Fourier temp = fourier[i];
        fourier[i] = fourier[j];
        fourier[j] = temp;
      }
    }
  }
}
