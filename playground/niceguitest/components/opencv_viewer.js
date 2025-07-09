export default {
    template: `<img :src="endpoint" />`,
    props: ['endpoint'],
    mounted() {
        console.log('OpenCV Viewer mounted, src=', this.endpoint);
    }
};