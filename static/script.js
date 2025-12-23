let photos = [];
let currentIndex = 0;
let startX = 0;
let isDragging = false;
let siteData = null;
let autoplayInterval = null;

function getSlugFromURL() {
    const path = window.location.pathname;
    const parts = path.split('/').filter(part => part.length > 0);
    const slug = parts[parts.length - 1];
    console.log('Extracted slug:', slug);
    return slug;
}

async function loadSiteData() {
    const slug = getSlugFromURL();
    console.log('Loading data for slug:', slug);
    
    try {
        const response = await fetch(`/api/site/${slug}`);
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            console.error('Response not OK');
            showError();
            return;
        }
        
        siteData = await response.json();
        console.log('Site data loaded:', siteData);
        renderSite();
    } catch (error) {
        console.error('Error loading site:', error);
        showError();
    }
}

function showError() {
    document.getElementById('loading').classList.add('hidden');
    document.getElementById('error').classList.remove('hidden');
    document.getElementById('content').classList.add('hidden');
}

function renderSite() {
    console.log('Rendering site...');
    document.getElementById('loading').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');
    document.getElementById('content').classList.remove('hidden');
    
    renderTitle();
    renderCarousel();
    renderCounter();
    renderMessage();
    renderMoments();
    renderFinalMessage();
    renderMusicPlayer();
}

function renderTitle() {
    const title = document.getElementById('title');
    title.textContent = `Para ${siteData.nome_homenageada}, com amor — ${siteData.nome_presenteador} 💖`;
}

function renderCarousel() {
    photos = siteData.fotos;
    const carousel = document.getElementById('carousel');
    const indicators = document.getElementById('indicators');
    
    carousel.innerHTML = '';
    indicators.innerHTML = '';
    
    photos.forEach((photo, index) => {
        const item = document.createElement('div');
        item.className = 'carousel-item';
        item.style.backgroundImage = `url(${photo})`;
        carousel.appendChild(item);
        
        const indicator = document.createElement('div');
        indicator.className = `indicator ${index === 0 ? 'active' : ''}`;
        indicator.addEventListener('click', () => goToSlide(index));
        indicators.appendChild(indicator);
    });
    
    document.getElementById('prevBtn').addEventListener('click', prevSlide);
    document.getElementById('nextBtn').addEventListener('click', nextSlide);
    
    const carouselContainer = document.querySelector('.carousel-container');
    carouselContainer.addEventListener('touchstart', handleTouchStart, false);
    carouselContainer.addEventListener('touchmove', handleTouchMove, false);
    carouselContainer.addEventListener('touchend', handleTouchEnd, false);
    
    startAutoplay();
}

function updateCarousel() {
    const carousel = document.getElementById('carousel');
    carousel.style.transform = `translateX(-${currentIndex * 100}%)`;
    
    const indicators = document.querySelectorAll('.indicator');
    indicators.forEach((indicator, index) => {
        indicator.classList.toggle('active', index === currentIndex);
    });
}

function goToSlide(index) {
    currentIndex = index;
    updateCarousel();
    resetAutoplay();
}

function nextSlide() {
    currentIndex = (currentIndex + 1) % photos.length;
    updateCarousel();
    resetAutoplay();
}

function prevSlide() {
    currentIndex = (currentIndex - 1 + photos.length) % photos.length;
    updateCarousel();
    resetAutoplay();
}

function handleTouchStart(e) {
    startX = e.touches[0].clientX;
    isDragging = true;
}

function handleTouchMove(e) {
    if (!isDragging) return;
}

function handleTouchEnd(e) {
    if (!isDragging) return;
    
    const endX = e.changedTouches[0].clientX;
    const diff = startX - endX;
    
    if (Math.abs(diff) > 50) {
        if (diff > 0) {
            nextSlide();
        } else {
            prevSlide();
        }
    }
    
    isDragging = false;
}

function startAutoplay() {
    if (autoplayInterval) {
        clearInterval(autoplayInterval);
    }
    autoplayInterval = setInterval(() => {
        nextSlide();
    }, 5000);
}

function resetAutoplay() {
    if (autoplayInterval) {
        clearInterval(autoplayInterval);
    }
    startAutoplay();
}

function renderCounter() {
    const startDate = new Date(siteData.data_inicio_relacionamento);
    const now = new Date();
    
    let years = now.getFullYear() - startDate.getFullYear();
    let months = now.getMonth() - startDate.getMonth();
    let days = now.getDate() - startDate.getDate();
    
    if (days < 0) {
        months--;
        const prevMonth = new Date(now.getFullYear(), now.getMonth(), 0);
        days += prevMonth.getDate();
    }
    
    if (months < 0) {
        years--;
        months += 12;
    }
    
    const counter = document.getElementById('counter');
    counter.innerHTML = `
        <div class="counter-item">
            <span class="counter-number">${years}</span>
            <span class="counter-label">${years === 1 ? 'Ano' : 'Anos'}</span>
        </div>
        <div class="counter-item">
            <span class="counter-number">${months}</span>
            <span class="counter-label">${months === 1 ? 'Mês' : 'Meses'}</span>
        </div>
        <div class="counter-item">
            <span class="counter-number">${days}</span>
            <span class="counter-label">${days === 1 ? 'Dia' : 'Dias'}</span>
        </div>
    `;
}

function renderMessage() {
    const mainMessage = document.getElementById('mainMessage');
    const signature = document.getElementById('signature');
    
    mainMessage.textContent = siteData.mensagem_principal;
    signature.textContent = `Com amor, ${siteData.nome_presenteador}`;
}

function renderMoments() {
    if (!siteData.momentos || siteData.momentos.length === 0) {
        return;
    }
    
    const momentsSection = document.getElementById('momentsSection');
    const momentsGrid = document.getElementById('moments');
    
    momentsSection.classList.remove('hidden');
    
    siteData.momentos.forEach(momento => {
        const card = document.createElement('div');
        card.className = 'moment-card';
        
        const date = new Date(momento.data);
        const formattedDate = date.toLocaleDateString('pt-BR', {
            day: '2-digit',
            month: 'long',
            year: 'numeric'
        });
        
        card.innerHTML = `
            <div class="moment-date">${formattedDate}</div>
            <div class="moment-description">${momento.descricao_curta}</div>
        `;
        
        momentsGrid.appendChild(card);
    });
}

function renderFinalMessage() {
    if (!siteData.mensagem_final) {
        return;
    }
    
    const finalMessageSection = document.getElementById('finalMessageSection');
    const finalMessage = document.getElementById('finalMessage');
    
    finalMessageSection.classList.remove('hidden');
    finalMessage.textContent = siteData.mensagem_final;
}

function renderMusicPlayer() {
    if (!siteData.musica) {
        return;
    }
    
    const musicPlayer = document.getElementById('musicPlayer');
    const audioPlayer = document.getElementById('audioPlayer');
    const playPauseBtn = document.getElementById('playPauseBtn');
    const musicLabel = document.getElementById('musicLabel');
    
    musicPlayer.classList.remove('hidden');
    
    if (siteData.musica.includes('youtube.com') || siteData.musica.includes('youtu.be')) {
        musicLabel.textContent = 'Ver vídeo';
        playPauseBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M19.615 3.637c-3.879-3.879-10.162-3.879-14.042 0-3.879 3.879-3.879 10.162 0 14.042 3.879 3.879 10.162 3.879 14.042 0 3.879-3.879 3.879-10.162 0-14.042zM10.5 14.5v-5l4 2.5-4 2.5z"></path></svg>';
        musicPlayer.addEventListener('click', () => {
            window.open(siteData.musica, '_blank');
        });
    } else {
        audioPlayer.src = siteData.musica;
        
        playPauseBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            
            if (audioPlayer.paused) {
                audioPlayer.play();
                playPauseBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"></path></svg>';
                musicLabel.textContent = 'Pausar música';
            } else {
                audioPlayer.pause();
                playPauseBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"></path></svg>';
                musicLabel.textContent = 'Tocar música';
            }
        });
    }
}

console.log('Script loaded, waiting for DOMContentLoaded...');
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, calling loadSiteData...');
    loadSiteData();
});
