Fourier[] dft(float[] x) {
    int N = x.length;
    Fourier[] fourier = new Fourier[N];
    for (int k = 0; k < N; k++) {
        float real = 0;
        float imag = 0;
        for (int n = 0; n < N; n++) {
            float phi = TWO_PI * k * n / N;
            real += x[n] * cos(phi);
            imag -= x[n] * sin(phi);
        }
        real = real / N;
        imag = imag / N;

        float freq = k;
        float magnitude = sqrt(real * real + imag * imag);
        float phase = atan2(imag, real);
        fourier[k] = new Fourier(real, imag, magnitude, phase, freq);
    }
    return fourier;
}

class Fourier {
    float real;
    float imag;
    float amp;
    float phase;
    float freq;
    
    Fourier(float r, float img, float a, float p, float f) {
        real = r;
        imag = img;
        amp = a;
        phase = p;
        freq= f;
    }

    float getFreq() {
        return this.freq;
    }

    float getReal() {
        return this.real;
    }

    float getImag() {
        return this.imag;
    }

    float getAmp() {
        return this.amp;
    }

    float getPhase() {
        return this.phase;
    }
}