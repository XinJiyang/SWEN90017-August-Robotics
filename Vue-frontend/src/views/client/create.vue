<template>
  <ClientForm mode="edit" @create-client="createClient" />
</template>

<script setup lang="ts">
import type { IClient } from '@/types';
import ClientForm from './components/client-form.vue';
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import type { AxiosError } from 'axios';
import { clientAddRequest } from '@/service/client/client';

const router = useRouter();

// function to create new client
function createClient(client: IClient) {
  // confirmation
  ElMessageBox.confirm('Are you sure you want to create a new client?', 'Confirmation', {
    confirmButtonText: 'Yes',
    cancelButtonText: 'Cancel',
    type: 'warning',
    center: true,
    roundButton: true,
    beforeClose: async (action, instance, done) => {
      if (action === 'confirm') {
        // activate loading animation
        instance.confirmButtonLoading = true;
        instance.confirmButtonText = 'Loading...';

        try {
          // send request
          await clientAddRequest(client);

          // request success
          instance.confirmButtonLoading = false;
          done();
          ElMessage.success('Add new client successfully.');
          router.push('/client');
        } catch (error) {
          // request fail
          if ((error as AxiosError).response?.status === 400) {
            ElMessage.error('Fail to add new client.');
          }
        }
      } else {
        done();
      }
    }
  });
}
</script>
