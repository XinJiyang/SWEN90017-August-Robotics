<template>
  <ClientForm mode="edit" @update-client="updateClient" />
</template>

<script setup lang="ts">
import type { IClient } from '@/types';
import ClientForm from './components/client-form.vue';
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import type { AxiosError } from 'axios';
import { clientEditRequest } from '@/service/client/client';

const router = useRouter();

// function to update client info
function updateClient(client: IClient) {
  // confirmation
  ElMessageBox.confirm('Are you sure you want to update client detail?', 'Confirmation', {
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
          await clientEditRequest(client);

          // request success
          instance.confirmButtonLoading = false;
          done();
          ElMessage.success('Update client detail successfully.');
          router.push('/client');
        } catch (error) {
          // request fail
          if ((error as AxiosError).response?.status === 400) {
            ElMessage.error('Fail to update client detail.');
          }
        }
      } else {
        done();
      }
    }
  });
}
</script>
