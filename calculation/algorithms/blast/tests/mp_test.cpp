#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <vector>
#include <iostream>

int
main(int argc, char *argv[])
{
    int i, n, id, chunk_size;

    n = 10;
    chunk_size = 2;

    printf("Liczba CPU: %d\n", omp_get_num_procs());

    #pragma omp parallel default(none) private(i, id) shared(n, chunk_size)
    {
        #pragma omp single
        {
            printf("SINGLE: Program jest wykonywany na %d watkach.\n",
                omp_get_num_threads());
        }

        printf("Program jest wykonywany na %d watkach.\n",
                        omp_get_num_threads());

        printf("OpenMP moze chodzic max na %d watkach.\n",
        		omp_get_max_threads());

        omp_set_num_threads(4);

        //#pragma omp for schedule(static, chunk_size)
		#pragma omp parallel for num_threads(4)
        for (i = 0; i < n; i++) {
            id = omp_get_thread_num();
            printf("Iteracja %d wykonana przez watek nr. %d.\n", i, id);
        }
    }

    return 0;
}
