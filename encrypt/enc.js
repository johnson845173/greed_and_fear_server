<script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
<script>
 var encrypted ='gfp6wzvTH3lN5TO2B37yWQ=='; //python is base64 ECB
 var key ='AAAAAAAAAAAAAAAA'//key used in Python
 key = CryptoJS.enc.Utf8.parse(key); 
 var decrypted =  CryptoJS.AES.decrypt(encrypted, key {mode:CryptoJS.mode.ECB});
 console.log(decrypted.toString(CryptoJS.enc.Utf8));
</script>