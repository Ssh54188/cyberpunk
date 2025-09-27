/**
 * 赛博朋克风格专用JavaScript文件 - 简化版
 * 仅包含基本的赛博朋克视觉效果
 */

// DOM就绪函数
function domReady(callback) {
    if (document.readyState !== 'loading') {
        callback();
    } else {
        document.addEventListener('DOMContentLoaded', callback);
    }
}

// 页面加载完成后执行
(function() {
    domReady(function() {
        // 初始化基础赛博朋克风格效果
        initBasicCyberpunkEffects();
    });
})();

/**
 * 初始化基础赛博朋克效果
 */
function initBasicCyberpunkEffects() {
    // 添加扫描线效果
    addScanlines();
    
    // 简化的霓虹效果
    initSimpleNeonEffects();
    
    // 添加轻微的全局动画
    addGlobalAnimation();
}

/**
 * 添加扫描线效果
 */
function addScanlines() {
    // 创建扫描线覆盖层
    const scanlines = document.createElement('div');
    scanlines.id = 'scanlines';
    scanlines.style.position = 'fixed';
    scanlines.style.top = '0';
    scanlines.style.left = '0';
    scanlines.style.width = '100%';
    scanlines.style.height = '100%';
    scanlines.style.pointerEvents = 'none';
    scanlines.style.zIndex = '9999';
    // 使用单行字符串或模板字符串
    scanlines.style.background = 'repeating-linear-gradient(transparent, rgba(0, 0, 0, 0.03) 1px, transparent 2px);'
    
    document.body.appendChild(scanlines);
}

/**
 * 初始化简化的霓虹效果
 */
function initSimpleNeonEffects() {
    const neonElements = document.querySelectorAll('.neon-text, .neon-border, h1, h2, h3');
    
    neonElements.forEach(element => {
        // 添加简单的霓虹效果
        element.style.textShadow = '0 0 5px #0ff, 0 0 10px #0ff';
        
        // 鼠标悬停增强效果
        element.addEventListener('mouseenter', function() {
            this.style.textShadow = '0 0 5px #0ff, 0 0 10px #0ff, 0 0 15px #0ff';
            this.style.transition = 'all 0.3s ease';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.textShadow = '0 0 5px #0ff, 0 0 10px #0ff';
        });
    });
}

/**
 * 添加全局动画效果
 */
function addGlobalAnimation() {
    // 轻微的背景脉动效果
    let pulseIntensity = 0;
    let pulseDirection = 0.02;
    
    function pulseBackground() {
        pulseIntensity += pulseDirection;
        if (pulseIntensity > 1 || pulseIntensity < 0) {
            pulseDirection *= -1;
        }
        
        // 应用到特定元素
        const accentElements = document.querySelectorAll('.accent, .featured-post');
        accentElements.forEach(el => {
            el.style.boxShadow = `0 0 ${5 + pulseIntensity * 5}px rgba(0, 255, 255, 0.3)`;
        });
        
        requestAnimationFrame(pulseBackground);
    }
    
    // 开始背景脉动动画
    pulseBackground();
}