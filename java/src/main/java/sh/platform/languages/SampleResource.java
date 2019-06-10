package sh.platform.languages;

import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Locale;
import java.util.Optional;

@RestController
@RequestMapping("java")
public class SampleResource {


    @GetMapping("{id}")
    public ResponseEntity<String> getSource(@PathVariable("id") String id) {
        final Optional<SampleCodeType> codeType = SampleCodeType.parse(id.toUpperCase(Locale.US));

        if (codeType.isPresent()) {

            SampleCode sampleCode = SampleCodeType.getSample(codeType.get());

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.TEXT_PLAIN);
            return new ResponseEntity<>(sampleCode.getSource(), headers, HttpStatus.OK);
        } else {
            return notFound();
        }
    }

    @GetMapping("{id}/output")
    public ResponseEntity<String> getExecuteCode(@PathVariable("id") String id) {
        final Optional<SampleCodeType> codeType = SampleCodeType.parse(id.toUpperCase(Locale.US));
        return codeType
                .map(SampleCodeStatus::of)
                .map(this::toResponseEntity)
                .orElse(notFound());
    }

    private ResponseEntity<String> notFound() {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.TEXT_PLAIN);
        return new ResponseEntity<>("Sorry, no sample code is available.", headers, HttpStatus.NOT_FOUND);
    }

    private ResponseEntity<String> toResponseEntity(SampleCodeStatus status) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.TEXT_PLAIN);
        if (status.isSuccess()) {
            return new ResponseEntity<>(status.getOutput(), headers, HttpStatus.OK);
        } else {
            return new ResponseEntity<>(status.getOutput(), headers, HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}
