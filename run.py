# -*- coding: utf-8 -*-
# Author: Vladimir Pichugin <vladimir@pichug.in>
import time
import threading

import main


if __name__ == "__main__":
    main.logger.debug("Initializing schedule parser..")

    thread_schedule = threading.Thread(target=main.schedule_parser)
    thread_schedule.setName('ScheduleThread')
    thread_schedule.daemon = True
    thread_schedule.start()

    # Поддерживать работу основной программы.
    while True:
        try:
            if not thread_schedule.is_alive():
                main.logger.error("Schedule thread is not alive, shutting down..")
                break

            time.sleep(10)
        except KeyboardInterrupt:
            main.logger.info("Shutting down..")
            break
