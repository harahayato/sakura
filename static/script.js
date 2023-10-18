'use strict'

//上に流れ続けるハートの実装
$(document).ready(function() {
    setInterval(function() {
      $('.heart-image-wrap').fadeIn(500);
      setTimeout(function() {
        $('.heart-image-wrap').fadeOut(500);
      }, 9000)
    }, 10000)
  });
  
  //回転するハートの画像を生成する
  function createRotateHeart() {
    const divElement = document.createElement('div');
    const innerElement = document.createElement('div');
    let selectNumberX = selectNumber();
    let selectNumberY = selectNumber();
  
    divElement.classList.add('heart-image-wrap');
    divElement.style.bottom = `${selectNumberY}%`;
    divElement.style.right = `${selectNumberX}%`;
    innerElement.classList.add('heart-image');
    innerElement.innerHTML = `
    <img src="static/images/heart_pink.png">
    `;
  
    divElement.appendChild(innerElement);
  
    document.body.appendChild(divElement);
  
    setTimeout(() => {
      divElement.remove();
    }, 10000);
  }
  
  //普通のハートを生成する
  function createNormalHeart() {
    const divElement = document.createElement('div');
    const innerElement = document.createElement('div');
    let selectNumberX = selectNumber();
    let selectNumberY = selectNumber();
  
    divElement.classList.add('Heart-image-wrap');
    divElement.style.bottom = `${selectNumberY}%`;
    divElement.style.right = `${selectNumberX}%`;
    innerElement.classList.add('Heart-image');
    innerElement.innerHTML = `
    <img src="static/images/heart_pink.png">
    `;
  
    divElement.appendChild(innerElement);
  
    document.body.appendChild(divElement);
  
    setTimeout(() => {
      divElement.remove();
    }, 10000);
  }
  //ランダムな位置に出現させるための設定
  function selectNumber () {
    let randomNumber = Math.trunc(Math.random() * 100)
    return randomNumber;
  }
  
  setInterval(createRotateHeart, 3000);
  setInterval(createNormalHeart, 1000);