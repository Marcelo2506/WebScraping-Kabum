FROM python:3.12-slim

# Instala dependências básicas
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg ca-certificates fonts-liberation libasound2 libatk-bridge2.0-0 \
    libatk1.0-0 libatspi2.0-0 libcups2 libdbus-1-3 libdrm2 libgbm1 libgtk-3-0 \
    libnspr4 libnss3 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 \
    libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 \
    libxtst6 lsb-release xdg-utils libu2f-udev libvulkan1 \
    && rm -rf /var/lib/apt/lists/*

# Instala Google Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get update && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb

# Descobre versão do Chrome instalada
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') \
    && CHROME_MAJOR=$(echo $CHROME_VERSION | cut -d. -f1) \
    && echo "Instalando ChromeDriver para versão $CHROME_MAJOR" \
    && DRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_$CHROME_MAJOR") \
    && wget -q https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${DRIVER_VERSION}/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && rm -rf chromedriver-linux64.zip /tmp/chromedriver-linux64


# Define variáveis de ambiente
ENV CHROME_BIN=/usr/bin/google-chrome
ENV PATH="/usr/bin:${PATH}"

# Cria diretório do app
WORKDIR /app

# Copia requirements.txt e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Comando padrão
CMD ["python", "Extract.py"]
