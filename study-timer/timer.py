from utime import sleep, ticks_ms, ticks_diff
import uasyncio

async def __count_down(duration_in_ms, should_stop, async_tasks):
    t_start = ticks_ms()
    while should_stop() is False:
        remain = duration_in_ms - ticks_diff(ticks_ms(), t_start)
        remain = max(remain, 0)
        remain_in_sec = round(remain / 1000)
        scheduled_tasks = []
        for task in async_tasks:
            scheduled_tasks.append(uasyncio.create_task(task(remain_in_sec)))
        if remain_in_sec == 0:
            # wait for all tasks in the last batch to finish before return
            for sche in scheduled_tasks:
                await sche
            return
        await uasyncio.sleep(1)

def count_down(duration_in_ms, should_stop, async_tasks):
    uasyncio.run(__count_down(duration_in_ms, should_stop, async_tasks))