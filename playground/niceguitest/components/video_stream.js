export default {
    template: `<canvas style="width:100%;height:auto;"></canvas>`,
    props: ['endpoint'],
    mounted() {
        // the component root ($el) is a wrapper element, so select the actual <canvas>
        const host = this.$el;
        const canvas = host.tagName === 'CANVAS'
            ? host
            : host.querySelector('canvas');

        console.log('📹 <video-stream> mounted! canvas=', canvas);
        const ctx = canvas.getContext('2d');
        const scheme = location.protocol === 'https:' ? 'wss' : 'ws';
        const ws = new WebSocket(`${scheme}://${location.host}${this.endpoint}`);
        ws.binaryType = 'arraybuffer';

        ws.onopen = () => console.log('WebSocket connected:', this.endpoint);
        ws.onmessage = ({data}) => {
            const dv = new DataView(data);
            const w = dv.getUint32(0);
            const h = dv.getUint32(4);
            const pixels = new Uint8ClampedArray(data, 8);
            canvas.width = w;
            canvas.height = h;
            ctx.putImageData(new ImageData(pixels, w, h), 0, 0);
        };
        ws.onerror = e => console.error('WebSocket error:', e);
        ws.onclose = () => console.log('WebSocket closed');
    }
};