<template class="m-0 p-0 w-100 ">
    <div class="gochi-hand-regular app-container" >
        <TopHeader class="m-0 p-0 w-100 "></TopHeader>
        <RouterView class="w-100 router-view" ></RouterView>
        <BottomFooter class="m-0 p-0 w-100 "></BottomFooter>
    </div>

</template>


<script setup lang="ts">
import TopHeader from '@/components/TopHeader.vue'
import BottomFooter from '@/components/BottomFooter.vue'
</script>

<style lang="css">
@import url('https://fonts.googleapis.com/css2?family=Gochi+Hand&display=swap');

* {
    box-sizing: border-box;
}


.gochi-hand-regular {
    font-family: "Gochi Hand", cursive;
    font-weight: 600;
    font-style: normal;
}

.app-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh; /* 整个视口高度，包含头部*/
}

/* RouterView 占据剩余空间 */
.router-view {
    flex: 1; /* 占据主内容区域的剩余空间 */
    overflow: auto; /* 如果内容过多，允许滚动 */
}


</style>

