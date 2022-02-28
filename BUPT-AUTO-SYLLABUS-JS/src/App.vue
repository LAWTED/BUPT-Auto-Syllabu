<template>
  <notifications />
  <div class="font-sans">
    <div class="relative min-h-screen flex flex-col justify-center items-center bg-gray-100 p-8">
      <div class="relative sm:max-w-sm w-full">
        <div class="card bg-blue-400 shadow-lg  w-full h-full rounded-3xl absolute  transform -rotate-6"></div>
        <div class="card bg-red-400 shadow-lg  w-full h-full rounded-3xl absolute  transform rotate-6"></div>
        <div class="relative w-full rounded-3xl  px-6 py-4 bg-gray-100 shadow-md">
          <label for="" class="block mt-3 text-xl text-gray-700 text-center font-semibold">
            北邮课表转苹果原生日历
          </label>
          <p class="text-gray-300 text-sm">仅供iPhone, iPad的Safari浏览器中使用</p>
          <div class="mt-10">
            <div>
              <input type="id" v-model="id" placeholder="请输入学号" class="p-4 mt-1 block w-full border-blue-400 border-2 bg-gray-100 h-11 rounded-xl shadow-lg  ">
            </div>

            <div class="mt-7">
              <input type="password" v-model="pw" placeholder="请输入新教务密码" class="p-4 mt-1 block w-full border-blue-400 border-2 bg-gray-100 h-11 rounded-xl shadow-lg ">
            </div>

            <div class="mt-7 flex">
            </div>

            <div class="mt-7">
              <button @click="send" class="bg-blue-500 w-full py-3 rounded-xl text-white shadow-xl hover:shadow-inner focus:outline-none transition duration-500 ease-in-out  transform hover:-translate-x hover:scale-105">
                Login
              </button>
            </div>

            <div class="flex mt-7 items-center text-center">
              <hr class="border-gray-300 border-1 w-full rounded-md">
              <label class="block font-medium text-sm text-gray-600 w-full">
                BY LAWTED
              </label>
              <hr class="border-gray-300 border-1 w-full rounded-md">
            </div>
          </div>
          <button @click='openurl' v-show="src !== ''" class="bg-blue-500 w-full py-3 rounded-xl text-white shadow-xl hover:shadow-inner focus:outline-none transition duration-500 ease-in-out  transform hover:-translate-x hover:scale-105 mt-4">点击查看课表</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";
import { notify } from "@kyvg/vue3-notification";

const id = ref("");
const pw = ref("");
const src = ref("");
const send = () => {
  if (id.value === "" || pw.value === "") {
    notify({
      type: 'warn',
      text: 'Please check your inputs'
    });
  } else {
    axios({
      url: '/api/login/',
      params: {
        id: id.value,
        pw: pw.value
      }
    }).then((res) => {
      src.value = res.data
    })
    // axios.get('/api/login')
    notify({
      type: 'success',
      text: 'Login in success'
    });
  }
};
const openurl = () => {
  window.open(src.value, "_blank");
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>

