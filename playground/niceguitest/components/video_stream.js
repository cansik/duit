export default {
    template: `<canvas style="width:100%;height:auto;"></canvas>`,
    props: ['endpoint'],
    data() {
        return {imageData: null, animationScheduled: false};
    },
    mounted() {
        const host = this.$el;
        const canvas = host.tagName === 'CANVAS' ? host : host.querySelector('canvas');
        console.log('📹 <video-stream> mounted! canvas=', canvas);
        const ctx = canvas.getContext('2d');
        const scheme = location.protocol === 'https:' ? 'wss' : 'ws';
        const ws = new WebSocket(`${scheme}://${location.host}${this.endpoint}`);
        ws.binaryType = 'arraybuffer';

        ws.onopen = () => console.log('WebSocket connected:', this.endpoint);
        ws.onmessage = ({data}) => {
            const dv = new DataView(data);
            const w = dv.getUint32(0), h = dv.getUint32(4);
            const pixels = new Uint8ClampedArray(data, 8);
            if (!this.imageData) {
                canvas.width = w;
                canvas.height = h;
                this.imageData = new ImageData(w, h);
            }
            this.imageData.data.set(pixels);
            if (!this.animationScheduled) {
                this.animationScheduled = true;
                requestAnimationFrame(() => {
                    ctx.putImageData(this.imageData, 0, 0);
                    this.animationScheduled = false;
                });
            }
        };
        ws.onerror = e => console.error('WebSocket error:', e);
        ws.onclose = () => console.log('WebSocket closed');
    }
};