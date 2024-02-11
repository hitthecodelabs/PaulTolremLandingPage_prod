async function connectMetaMask() {
  if (window.ethereum) {
    try {
      // Request account access
      await window.ethereum.request({ method: 'eth_requestAccounts' });
    } catch (error) {
      // User denied account access
      console.error('User denied account access');
    }
  } else {
    console.error('Non-Ethereum browser detected. You should consider trying MetaMask!');
  }
}
