using Microsoft.AspNetCore.HttpOverrides;
using TenderGuard.Api.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var agentApiBaseUrl =
    Environment.GetEnvironmentVariable("AGENT_API_BASE_URL")
    ?? builder.Configuration["AgentApi:BaseUrl"]
    ?? "http://localhost:8001";

if (!agentApiBaseUrl.EndsWith("/"))
{
    agentApiBaseUrl += "/";
}

builder.Services.AddHttpClient<AgentApiClient>(client =>
{
    client.BaseAddress = new Uri(agentApiBaseUrl);
});

builder.Services.AddSingleton<ReviewService>();

var allowedOriginsValue =
    Environment.GetEnvironmentVariable("CORS_ALLOWED_ORIGINS")
    ?? builder.Configuration["Cors:AllowedOrigins"]
    ?? "http://localhost:5173";

var allowedOrigins = allowedOriginsValue
    .Split(',', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)
    .Where(origin => Uri.TryCreate(origin, UriKind.Absolute, out _))
    .ToArray();

builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowFrontend", policy =>
    {
        policy
            .WithOrigins(allowedOrigins)
            .AllowAnyHeader()
            .AllowAnyMethod();
    });
});

var app = builder.Build();

app.UseForwardedHeaders(new ForwardedHeadersOptions
{
    ForwardedHeaders = ForwardedHeaders.XForwardedFor | ForwardedHeaders.XForwardedProto
});

app.UseSwagger();
app.UseSwaggerUI();

app.UseHttpsRedirection();
app.UseCors("AllowFrontend");

app.MapGet("/", () => Results.Ok(new
{
    service = "TenderGuard .NET Backend",
    status = "running"
}));

app.UseAuthorization();
app.MapControllers();

app.Run();
