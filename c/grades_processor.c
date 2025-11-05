#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define MAX 1000

double mean(double arr[], int n)
{
    double sum = 0;
    for (int i = 0; i < n; i++)
        sum += arr[i];
    return sum / n;
}

double median(double arr[], int n)
{
    for (int i = 0; i < n - 1; i++)
        for (int j = i + 1; j < n; j++)
            if (arr[i] > arr[j])
            {
                double tmp = arr[i];
                arr[i] = arr[j];
                arr[j] = tmp;
            }
    if (n % 2 == 0)
        return (arr[n / 2 - 1] + arr[n / 2]) / 2;
    else
        return arr[n / 2];
}

double stddev(double arr[], int n)
{
    double m = mean(arr, n);
    double sum = 0;
    for (int i = 0; i < n; i++)
        sum += (arr[i] - m) * (arr[i] - m);
    return sqrt(sum / n);
}

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        printf("Uso: %s arquivo.csv\n", argv[0]);
        return 1;
    }

    FILE *f = fopen(argv[1], "r");
    if (!f)
    {
        printf("Erro ao abrir %s\n", argv[1]);
        return 1;
    }

    double notas[MAX];
    int n = 0;
    while (fscanf(f, "%lf,", &notas[n]) == 1)
    {
        n++;
    }
    fclose(f);

    printf("Total de notas: %d\n", n);
    printf("Média: %.2f\n", mean(notas, n));
    printf("Mediana: %.2f\n", median(notas, n));
    printf("Desvio padrão: %.2f\n", stddev(notas, n));

    return 0;
}
