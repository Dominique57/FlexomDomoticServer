'use strict';

function urlB64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
        .replace(/\-/g, '+')
        .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
}

function checkBrowserCompatibility() {
    if (!('serviceWorker' in navigator))
      return 'ServiceWorker';
    if (!('PushManager' in window))
        return 'PushManager';
    return '';
}

async function tryRegisterServiceWorker() {
    let registration = null;
    try {
        registration = await navigator.serviceWorker.register('/static/sw.js');
    } catch (err) {
        return [null, err];
    }
    return [registration, null];
}

async function askNotificationPermission() {
    const permissionPromise = new Promise(function (resolve, reject) {
        const permissionResult = Notification.requestPermission(function (result) {
            resolve(result);
        });
        if (permissionResult)
            permissionResult.then(resolve, reject);
    })
    return await permissionPromise;
}

async function fetchApplicationServerKey() {
    let public_key = null;
    try {
        const response = await fetch("subscription/", {
            method: 'GET',
        });
        const responseJson = await response.json();
        public_key = responseJson.public_key;
    } catch (err) {
        return [null, err];
    }
    return [public_key, null]
}

async function subscribeUserToPush(registration, serverKey) {
    const subscribeOptions = {
        userVisibleOnly: true,
        applicationServerKey: urlB64ToUint8Array(serverKey),
    };
    let pushSubscription;
    try {
        pushSubscription = await registration.pushManager.subscribe(subscribeOptions);
    } catch (err) {
        return [null, err];
    }
    return [pushSubscription, null];
}

async function sendUserSubscription(subscription) {
    let res;
    try {
        res = await fetch("subscription/", {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(subscription),
        });
    } catch (err) {
        return 'Failed to execute post request `' + err + '` !';
    }
    if (!res.ok) {
        return 'POST request failed (code: `' + res.status + '`), (body `' + res.body  + '`) !';
    }
    return ''
}

async function start() {
    // Check browser CAN handle web push
    const browserCompErr = checkBrowserCompatibility();
    if (browserCompErr !== '') {
        alert('Browser is not compatible, missing: "' + browserCompErr + '" !');
        return;
    }

    // try registering Service Worker
    const [registration, regErr] = await tryRegisterServiceWorker();
    if (regErr !== null) {
        alert('Browser failed to register service worker: `' + regErr + '` !');
        return;
    }

    // Try getting notification access
    const notificationPermission = await askNotificationPermission();
    if (notificationPermission !== 'granted') {
        alert('Notification not granted, please reset permissions !');
        return;
    }

    // Fetch application server key
    const [serverKey, serverKeyFetchErr] = await fetchApplicationServerKey();
    if (serverKeyFetchErr !== null) {
        alert('Server failed to return application server key: `' + serverKeyFetchErr + '` !');
        return;
    }

    // Subscribe use to push
    const [pushSub, pushSubErr] = await subscribeUserToPush(registration, serverKey);
    if (pushSubErr !== null) {
        alert('Browser push subscription failed: `' + pushSubErr + '` !');
        return;
    }

    // Send subscription to server
    const sendSubErr = await sendUserSubscription(pushSub);
    if (sendSubErr !== '') {
        alert('Failed to send push subscription to server: `' + sendSubErr + '` !');
        return;
    }

    console.log(JSON.stringify(pushSub));
}
