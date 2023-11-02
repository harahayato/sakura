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


  //ローディング画面の設定

  var bar = new ProgressBar.Line(splash_text, {//id名を指定
    easing: 'easeInOut',//アニメーション効果linear、easeIn、easeOut、easeInOutが指定可能
    duration: 3000,//時間指定(1000＝1秒)
    strokeWidth: 0.2,//進捗ゲージの太さ
    color: 'pink',//進捗ゲージのカラー
    trailWidth: 0.2,//ゲージベースの線の太さ
    trailColor: '#fff',//ゲージベースの線のカラー
    text: {//テキストの形状を直接指定       
      style: {//天地中央に配置
        position: 'absolute',
        left: '50%',
        top: '50%',
        padding: '0',
        margin: '-60px 0 0 0',//バーより上に配置
        transform:'translate(-50%,-50%)',
        'font-size':'5rem',
        color: '#fff',
      },
      autoStyleContainer: false //自動付与のスタイルを切る
    },
    step: function(state, bar) {
      bar.setText(Math.round(bar.value() * 100) + ' %'); //テキストの数値
    }
  });
  
  //アニメーションスタート
  bar.animate(1.0, function () {//バーを描画する割合を指定します 1.0 なら100%まで描画します
    $("#splash_text").fadeOut(10);//フェイドアウトでローディングテキストを削除
    $(".loader_cover-up").addClass("coveranime");//カバーが上に上がるクラス追加
    $(".loader_cover-down").addClass("coveranime");//カバーが下に下がるクラス追加
    $("#splash").fadeOut();//#splashエリアをフェードアウト
  });



  //告白成功率のカウントアップ
  const shuffleNumberCounter = (target) => {
    const targetNum = Number(target.getAttribute('data-num'))
  
    let counterData = null
    const speed = 2000 / targetNum
    let initNum = 0
  
    const countUp = () => {
      if (Number.isInteger(targetNum)) {
        target.innerHTML = initNum + '%'
      } else {
        target.innerHTML = `${initNum}.${Math.floor(Math.random() * 9)}` + '%'
      }
  
      initNum++
  
      if (initNum > targetNum) {
        target.innerHTML = targetNum + '%'
        clearInterval(counterData)
      }

    }
    
    counterData = setInterval(countUp, speed)
  }
  
  const target = document.querySelector('.number');
  
  setTimeout(function(){shuffleNumberCounter(target)}, 3000)