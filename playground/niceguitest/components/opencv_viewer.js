export default {
    template: `<img :src="endpoint" style="width:100%; height:auto;" />`,
    props: ['endpoint'],
    mounted() {
        console.log('📹 <video-stream> MJPEG mounted, src=', this.endpoint);
    }
};