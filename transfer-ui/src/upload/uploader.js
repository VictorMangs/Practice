// upload/uploader.js

export async function uploadQueue({
  store,
  concurrency = 5,
  uploadFn,
  onProgressUpdate,
}) {
  let index = 0;
  let active = 0;

  return new Promise((resolve) => {
    const runNext = () => {
      if (index >= store.queue.length && active === 0) {
        resolve();
        return;
      }

      while (active < concurrency && index < store.queue.length) {
        const id = store.queue[index++];
        const file = store.files.get(id);

        active++;

        uploadFn(file, (progress) => {
          store.progress.set(id, progress);
          onProgressUpdate?.(id, progress);
        })
          .catch(() => {
            // retry (simple production baseline)
            store.queue.push(id);
          })
          .finally(() => {
            active--;
            runNext();
          });
      }
    };

    runNext();
  });
}